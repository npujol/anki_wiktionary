import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

from gtts import gTTS  # type: ignore

from app.anki_connectors import AnkiLocalConnector, AnkiWebConnector
from app.data_processors import NoteDataProcessor
from app.private_config import (
    anki_deck_name,
    anki_note_file_path,
    anki_password,
    anki_username,
    working_path,
)
from app.serializers import AudioItem, CustomFields, CustomNote

logger: logging.Logger = logging.getLogger(name=__name__)


async def generate_audio(text: str) -> Path:
    """
    Asynchronously generates audio for a given text.

    Args:
        text (str): The text to generate audio for.

    Returns:
        Path: The path to the generated audio file.
    """
    tts = gTTS(text=text, lang="de")  # type: ignore
    path: Path = working_path / f"{text}.mp3"
    tts.save(savefile=path)  # type: ignore
    return path


def add_audio(note: CustomNote) -> CustomNote:
    """
    Asynchronously retrieves Anki note data for a given word.

    Args:
        note (str): The Anki note data.

    Returns:
        NoteData: The Anki note data for the specified word.
    """
    tts = gTTS(text=note.word, lang="de")  # type: ignore
    path: Path = working_path / f"{note.word}.mp3"
    tts.save(savefile=path)  # type: ignore
    if note.fields is not None and isinstance(note.fields, CustomFields):
        note.audio = [
            AudioItem.model_validate(
                obj={
                    # This value is from the local server
                    "url": f"http://localhost:8000/{working_path}/{note.fields.full_word}.mp3",
                    "filename": f"{note.word}.mp3",
                    "skipHash": "true",
                    "fields": ["audio"],
                }
            )
        ]
    return note


def add_audio_local(note: CustomNote) -> CustomNote:
    """
    Asynchronously retrieves Anki note data for a given word.

    Args:
        note (str): The Anki note data.

    Returns:
        NoteData: The Anki note data for the specified word.
    """
    word: Callable[..., str] = note.word
    tts = gTTS(text=word, lang="de")  # type: ignore
    path: Path = working_path / f"{word}.mp3"
    tts.save(savefile=path)  # type: ignore
    note.audio = [
        AudioItem.model_validate(
            obj={
                # This value is from the local server
                "url": f"{working_path}/{word}.mp3",
                "filename": f"{word}.mp3",
                "skipHash": "true",
                "fields": ["audio"],
            }
        )
    ]
    return note


def generate_note(word: str) -> bool:
    """
    Generate Anki note for a given word and add it to Anki database.

    Args:
        word (str): The word for which the Anki note is to be created.

    Returns:
        bool: True if the Anki note is created successfully, False otherwise.
    """
    try:
        logger.info(msg=f"Creating Anki note for {word}")
        note: CustomNote | None = NoteDataProcessor(
            deck_name=anki_deck_name, model_name="Basic_"
        ).get_anki_note(word=word)

        if not note:
            logger.error(msg=f"Anki note for {word=} could not be created.")
            return False
        note = add_audio(note=note)
        id: dict[str, Any] = AnkiLocalConnector().add_note(note=note)
        logger.info(msg=f"Note of {word=} with {id=} was created.")
    except Exception as e:
        logger.exception(msg=f"Anki note for {word=} could not be created, due to {e}.")
        return False
    return True


async def get_anki_note_data(word: str) -> CustomNote | None:
    """
    Asynchronously retrieves Anki note data for a given word.

    Args:
        word (str): The word for which to retrieve Anki note data.

    Returns:
        NoteData: The Anki note data for the specified word.
    """
    note: CustomNote | None = NoteDataProcessor().get_anki_note(word=word)
    if note is not None:
        return add_audio(note=note)


async def save_anki_note_to_list(
    word: str, file_path: Path | str = anki_note_file_path
) -> bool:
    """
    Asynchronous function to save an Anki note to a list.

    Args:
        word (str): The word to be saved as a note.

    Returns:
        bool: True if the Anki note is saved successfully, False otherwise.
    """

    is_successful = False

    try:
        with open(file=file_path, mode="a") as file:
            file.write(f"{word}\n")
        logger.info(msg=f"Anki note created: {datetime.now().isoformat()}: {word}")

        is_successful = True
    except Exception as e:
        logger.exception(msg=f"Anki note could not be created, due to {e}.")
    return is_successful


def generate_notes(notes_path: Path | str = anki_note_file_path) -> bool:
    """
    A function to generate notes from a file and write them back to the file.
    """

    try:
        with open(file=notes_path, mode="r") as file:
            words: list[str] = file.readlines()
        for word in set(words):
            logger.info(msg=f"Generating Anki note for {word}")
            try:
                word: str = word.strip()
                generate_note(word=word)
            except Exception as e:
                logger.exception(msg=f"Anki notes, due to {e}.")
                continue
        with open(file=notes_path, mode="w") as file:
            words = file.truncate()  # type: ignore
    except Exception as e:
        logger.error(msg=f"Anki notes, due to {e}.")
        return False
    return True


async def send_card_using_anki_web(
    word: str,
    deck_name: str = anki_deck_name,
    model_name: str = "Basic_",
    processor_name: str = "wiktionary",
) -> Optional[CustomNote]:
    """
    Asynchronously sends an Anki note to AnkiWeb.

    Args:
        word (str): The word to be sent to AnkiWeb.
        deck_name (str, optional): The name of the deck. Defaults to "Mein Deutsch".
        model_name (str, optional): The name of the model. Defaults to "Basic_".
        processor_name (str, optional): The name of the processor.
        Defaults to "wiktionary".
    Returns:
        CustomNote: The Anki note that was sent to AnkiWeb.
    """
    username: str = anki_username
    password: str = anki_password

    if not username or not password:
        logger.error(msg="Username or password not set.")
        return

    # Create Anki note
    logger.info(msg=f"Creating Anki note for {word}")
    note: CustomNote | None = NoteDataProcessor(
        deck_name=deck_name,
        model_name=model_name,
    ).get_anki_note(
        word=word,
        processor_name=processor_name,
    )

    if not note:
        logger.error(msg=f"Anki note for {word=} could not be created.")
        return

    note = add_audio_local(note=note)

    # Send note to Anki web interface
    web_anki_connector = AnkiWebConnector(
        username=username,
        password=password,
    )
    logger.info(
        msg=(
            f"Sending Anki note for {word} to AnkiWeb using {deck_name=} "
            f"and {model_name}."
        )
    )
    web_anki_connector.start()
    is_successful: bool = web_anki_connector.send_card(
        custom_note=note,
        tags=[
            deck_name,
            model_name,
            datetime.now().isoformat(),
        ],
        card_type=note.card_type,  # type: ignore
    )
    web_anki_connector.close()

    if not is_successful:
        logger.error(msg=f"Anki note for {word=} could not be created.")
        return

    logger.info(msg=f"Note of {word=} was created successfully.")
    return note


if __name__ == "__main__":
    generate_notes()
