import logging
from datetime import datetime
from typing import Optional

from environs import Env
from gtts import gTTS  # type: ignore

from app.anki_connector import AnkiConnector
from app.ankiweb import WebAnkiConnector
from app.data_processor import NoteDataProcessor
from app.private_config import working_path
from app.serializers import AudioItem, CustomNote

env = Env()
env.read_env(override=True)


# File path to store Anki notes
ANKI_NOTES_FILE_PATH = env("ANKI_NOTES_FILE_PATH") or "anki_notes.txt"


logger = logging.getLogger(__name__)


async def generate_audio(text: str):
    tts = gTTS(text, lang="de")  # type: ignore
    path = working_path / f"{text}.mp3"
    tts.save(path)
    return path


def add_audio(note: CustomNote):
    """
    Asynchronously retrieves Anki note data for a given word.

    Args:
        note (str): The Anki note data.

    Returns:
        NoteData: The Anki note data for the specified word.
    """
    text = note.fields.full_word
    tts = gTTS(text, lang="de")  # type: ignore
    path = working_path / f"{text}.mp3"
    tts.save(path)
    note.audio = [
        AudioItem.model_validate(
            {
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
    text = note.fields.full_word
    tts = gTTS(text, lang="de")  # type: ignore
    path = working_path / f"{text}.mp3"
    tts.save(path)
    note.audio = [
        AudioItem.model_validate(
            {
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
        logger.info(f"Creating Anki note for {word}")
        note = NoteDataProcessor(
            deck_name="Mein Deutsch", model_name="Basic_"
        ).get_anki_note(word)

        if not note:
            logger.error(f"Anki note for {word=} could not be created.")
            return False
        note = add_audio(note)
        id = AnkiConnector().add_note(note)
        logger.info(f"Note of {word=} with {id=} was created.")
    except Exception as e:
        logger.exception(f"Anki note for {word=} could not be created, due to {e}.")
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
    note = NoteDataProcessor().get_anki_note(word)
    if note is not None:
        return add_audio(note)


async def save_anki_note_to_list(word: str) -> None:
    """
    Asynchronous function to save an Anki note to a list.

    Args:
        word (str): The word to be saved as a note.

    Returns:
        None
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ANKI_NOTES_FILE_PATH, "a") as file:
        file.write(f"{word}\n")
    logger.info(f"Anki note created: {timestamp}: {word}")


def generate_notes() -> bool:
    """
    A function to generate notes from a file and write them back to the file.
    """
    try:
        with open(ANKI_NOTES_FILE_PATH, "r") as file:
            words = file.readlines()
        for word in set(words):
            logger.info(f"Generating Anki note for {word}")
            try:
                word = word.strip()
                generate_note(word)
            except Exception as e:
                logger.exception(f"Anki notes, due to {e}.")
                continue
        with open(ANKI_NOTES_FILE_PATH, "w") as file:
            words = file.truncate()
    except Exception as e:
        logger.error(f"Anki notes, due to {e}.")
        return False
    return True


async def send_card_using_anki_web(
    word: str,
    deck_name: str = "Mein Deutsch",
    model_name: str = "Basic_",
) -> Optional[CustomNote]:
    """Sends an Anki note to the Anki web interface."""
    username = env.str("ANKI_USER") or None
    password = env.str("ANKI_PASS") or None

    if not username or not password:
        logger.error("Username or password not set.")
        return

    # Create Anki note
    logger.info(f"Creating Anki note for {word}")
    note = NoteDataProcessor(
        deck_name=deck_name,
        model_name=model_name,
    ).get_anki_note(word)

    if not note:
        logger.error(f"Anki note for {word=} could not be created.")
        return

    note = add_audio_local(note)

    # Send note to Anki web interface
    web_anki_connector = WebAnkiConnector(username, password)
    web_anki_connector.start()
    is_successful = web_anki_connector.send_card(
        note, [deck_name, model_name, datetime.now().isoformat()]
    )
    web_anki_connector.close()

    if not is_successful:
        logger.error(f"Anki note for {word=} could not be created.")
        return

    logger.info(f"Note of {word=} was created successfully.")
    return note


if __name__ == "__main__":
    generate_notes()
