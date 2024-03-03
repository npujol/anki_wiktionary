from app.connector import AnkiConnector
from app.data_processor import NoteDataProcessor
import logging

logger = logging.getLogger(__name__)


def generate_notes(word: str) -> bool:
    try:
        logger.info(f"Creating Anki note for {word}")
        note = NoteDataProcessor().get_anki_note(word)
        id = AnkiConnector().add_note(note)
        logger.info(f"Note of {word=} with {id=} was created.")
    except Exception as e:
        logger.exception(f"Anki note for {word=} could not be created, due to {e}.")
        return False
    return True
