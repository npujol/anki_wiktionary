import logging

from app.data_processor.wiktionary_data_processor import WiktionaryDataProcessor
from app.serializers import CustomFields, CustomNote

logger = logging.getLogger(name=__name__)


class NoteDataProcessor:
    def __init__(self, deck_name: str = "Test", model_name: str = "Basic_") -> None:
        self.data_handler = WiktionaryDataProcessor()
        self.deck_name = deck_name
        self.model_name = model_name

    def get_anki_note(self, word: str) -> CustomNote | None:
        # TODO:
        # - Review content using ollama
        # - Include missing values using ollama
        # - Get content from other sources
        # - Generate the complete content using ollama
        content = self.data_handler.get_wiktionary_data(word=word)
        note = CustomNote(
            deckName=self.deck_name,
            modelName=self.model_name,
            tags=["test"],
            audio=[],
            video=[],
            picture=[],
        ).import_from_content(content=content)

        return note
