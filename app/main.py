from datetime import datetime
from app.connector import AnkiConnector
from app.data_processor import NoteDataProcessor
import logging
from environs import Env


env = Env()
env.read_env()


# File path to store Anki notes
ANKI_NOTES_FILE_PATH = env("ANKI_NOTES_FILE_PATH") or "anki_notes.txt"


logger = logging.getLogger(__name__)


def generate_note(word: str) -> bool:
    try:
        logger.info(f"Creating Anki note for {word}")
        note = NoteDataProcessor().get_anki_note(word)
        id = AnkiConnector().add_note(note)
        logger.info(f"Note of {word=} with {id=} was created.")
    except Exception as e:
        logger.exception(f"Anki note for {word=} could not be created, due to {e}.")
        return False
    return True


async def get_anki_note_data(word: str):
    return NoteDataProcessor().get_anki_note(word)


# Function to save an Anki note
async def save_anki_note_to_list(word: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ANKI_NOTES_FILE_PATH, "a") as file:
        file.write(f"{word}\n")
    logger.info(f"Anki note created: {timestamp}: {word}")


def generate_notes() -> bool:
    try:
        with open(ANKI_NOTES_FILE_PATH, "r") as file:
            words = file.readlines()
        for word in words:
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
