import logging
from typing import Optional

from app.data_processors.processors.duden_data_processor import DudenDataProcessor
from app.data_processors.processors.ollama_data_processor import OllamaDataProcessor
from app.data_processors.processors.verben_data_processor import VerbenDataProcessor
from app.data_processors.processors.wiktionary_data_processor import (
    WiktionaryDataProcessor,
)
from app.serializers import CustomNote

PROCESSORS_MAP = {
    "wiktionary": WiktionaryDataProcessor(),
    "ollama": OllamaDataProcessor(),
    "verben": VerbenDataProcessor(),
    "duden": DudenDataProcessor(),
}
logger = logging.getLogger(name=__name__)


class NoteDataProcessor:
    def __init__(
        self,
        deck_name: str = "Test",
        model_name: str = "Basic_",
    ) -> None:
        self.deck_name = deck_name
        self.model_name = model_name

    # TODO: Check if the dict info is complete.
    def get_anki_note(
        self, word: str, processor_name: Optional[str] = "wiktionary"
    ) -> CustomNote | None:
        content = {}
        processor = None
        if not processor_name:
            for processor in PROCESSORS_MAP.values():
                content = processor.get_note_data(word=word)
                if content:
                    break
        else:
            processor = PROCESSORS_MAP[processor_name]
            content = processor.get_note_data(word=word)
        note = CustomNote(
            deckName=self.deck_name,
            modelName=self.model_name,
            tags=["test"],
            audio=[],
            video=[],
            picture=[],
        )
        if processor is not None:
            note = note.import_from_content(
                content=content,
                fields_class=processor.fields_class,
            )

        return note
