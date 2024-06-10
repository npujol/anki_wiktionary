import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from gtts import gTTS  # type: ignore

from app.anki_connector.anki_local_connector import AnkiLocalConnector
from app.anki_connector.anki_web_connector import AnkiWebConnector
from app.data_processor.note_data_processor import NoteDataProcessor
from app.private_config import (
    anki_note_file_path,
    anki_password,
    anki_username,
    working_path,
)
from app.serializers import AudioItem, CustomNote

logger = logging.getLogger(name=__name__)


async def generate_audio(text: str) -> Path:
    """
    Asynchronously generates audio for a given text.

    Args:
        text (str): The text to generate audio for.

    Returns:
        Path: The path to the generated audio file.
    """
    tts = gTTS(text=text, lang="de")  # type: ignore
    path = working_path / f"{text}.mp3"
    tts.save(savefile=path)
    return path


def add_audio(note: CustomNote) -> CustomNote:
    """
    Asynchronously retrieves Anki note data for a given word.

    Args:
        note (str): The Anki note data.

    Returns:
        NoteData: The Anki note data for the specified word.
    """
    text = note.fields.full_word
    tts = gTTS(text=text, lang="de")  # type: ignore
    path = working_path / f"{text}.mp3"
    tts.save(savefile=path)
    note.audio = [
        AudioItem.model_validate(
            obj={
                # This value is from the local server
                "url": f"http://localhost:8000/{working_path}/{note.fields.full_word}.mp3",
                "filename": f"{note.fields.full_word}.mp3",
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
    if not note.shall_add_audio:
        return note
    text = note.fields.full_word
    tts = gTTS(text=text, lang="de")  # type: ignore
    path = working_path / f"{text}.mp3"
    tts.save(savefile=path)
    note.audio = [
        AudioItem.model_validate(
            obj={
                # This value is from the local server
                "url": f"{working_path}/{note.fields.full_word}.mp3",
                "filename": f"{note.fields.full_word}.mp3",
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
        note = NoteDataProcessor(
            deck_name="Mein Deutsch", model_name="Basic_"
        ).get_anki_note(word=word)

        if not note:
            logger.error(msg=f"Anki note for {word=} could not be created.")
            return False
        note = add_audio(note=note)
        id = AnkiLocalConnector().add_note(note=note)
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
    note = NoteDataProcessor().get_anki_note(word=word)
    if note is not None:
        return add_audio(note=note)


async def save_anki_note_to_list(word: str) -> None:
    """
    Asynchronous function to save an Anki note to a list.

    Args:
        word (str): The word to be saved as a note.

    Returns:
        None
    """
    with open(file=anki_note_file_path, mode="a") as file:
        file.write(f"{word}\n")
    logger.info(msg=f"Anki note created: {datetime.now().isoformat()}: {word}")


def generate_notes() -> bool:
    """
    A function to generate notes from a file and write them back to the file.
    """
    try:
        with open(file=anki_note_file_path, mode="r") as file:
            words = file.readlines()
        for word in set(words):
            logger.info(msg=f"Generating Anki note for {word}")
            try:
                word = word.strip()
                generate_note(word=word)
            except Exception as e:
                logger.exception(msg=f"Anki notes, due to {e}.")
                continue
        with open(file=anki_note_file_path, mode="w") as file:
            words = file.truncate()
    except Exception as e:
        logger.error(msg=f"Anki notes, due to {e}.")
        return False
    return True


async def send_card_using_anki_web(
    word: str,
    deck_name: str = "Mein Deutsch",
    model_name: str = "Basic_",
    processor_name: str = "wiktionary",
) -> Optional[CustomNote]:
    """
    Asynchronously sends an Anki note to AnkiWeb.

    Args:
        word (str): The word to be sent to AnkiWeb.
        deck_name (str, optional): The name of the deck. Defaults to "Mein Deutsch".
        model_name (str, optional): The name of the model. Defaults to "Basic_".
        processor_name (str, optional): The name of the processor. Defaults to "wiktionary".
    Returns:
        CustomNote: The Anki note that was sent to AnkiWeb.
    """
    username = anki_username
    password = anki_password

    if not username or not password:
        logger.error(msg="Username or password not set.")
        return

    # Create Anki note
    logger.info(msg=f"Creating Anki note for {word}")
    note = NoteDataProcessor(
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
    web_anki_connector.start()
    is_successful = web_anki_connector.send_card(
        custom_note=note,
        tags=[
            deck_name,
            model_name,
            datetime.now().isoformat(),
        ],
        card_type=note.card_type,
    )
    web_anki_connector.close()

    if not is_successful:
        logger.error(msg=f"Anki note for {word=} could not be created.")
        return

    logger.info(msg=f"Note of {word=} was created successfully.")
    return note


if __name__ == "__main__":
    generate_notes()
