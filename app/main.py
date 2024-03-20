from datetime import datetime
from app.anki_connector import AnkiConnector
from app.data_processor import NoteDataProcessor
import logging
from environs import Env
from gtts import gTTS  # type: ignore
from pathlib import Path
from app.serializers import AudioItem, CustomNote


env = Env()
env.read_env()


# File path to store Anki notes
ANKI_NOTES_FILE_PATH = env("ANKI_NOTES_FILE_PATH") or "anki_notes.txt"


logger = logging.getLogger(__name__)


def add_audio(note: CustomNote):
    """
    Asynchronously retrieves Anki note data for a given word.

    Args:
        note (str): The Anki note data.

    Returns:
        NoteData: The Anki note data for the specified word.
    """
    tts = gTTS(note.fields.full_word, lang="de")  # type: ignore
    path = Path(__file__).parent.parent / f"files/{note.fields.full_word}.mp3"
    tts.save(path)
    note.audio = [
        AudioItem.model_validate(
            {
                # This value is from the local server
                "url": f"http://localhost:8000/files/{note.fields.full_word}.mp3",
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


if __name__ == "__main__":
    generate_notes()
