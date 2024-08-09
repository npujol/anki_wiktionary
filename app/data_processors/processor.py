import logging
from typing import Any, Optional

from app.data_processors.processors.base_data_processor import BaseDataProcessor
from app.data_processors.processors.duden_data_processor import DudenDataProcessor
from app.data_processors.processors.ollama_data_processor import OllamaDataProcessor
from app.data_processors.processors.verben_data_processor import VerbenDataProcessor
from app.data_processors.processors.wiktionary_data_processor import (
    WiktionaryDataProcessor,
)
from app.serializers import CustomNote

PROCESSORS_MAP: dict[
    str,
    BaseDataProcessor,
] = {
    "wiktionary": WiktionaryDataProcessor(),
    "verben": VerbenDataProcessor(),
    "duden": DudenDataProcessor(),
    "ollama": OllamaDataProcessor(),
}
logger: logging.Logger = logging.getLogger(name=__name__)


class NoteDataProcessor:
    def __init__(
        self,
        deck_name: str = "Test",
        model_name: str = "Basic_",
    ) -> None:
        self.deck_name: str = deck_name
        self.model_name: str = model_name

    # TODO: Check if the dict info is complete.
    def get_anki_note(
        self, word: str, processor_name: Optional[str] = None
    ) -> CustomNote | None:
        processor: BaseDataProcessor | None = None

        initial_note = CustomNote(
            deckName=self.deck_name,
            modelName=self.model_name,
            tags=["test"],
            audio=[],
            video=[],
            picture=[],
        )

        if not processor_name:
            updated_note = self._get_content_using_multiple_processors(
                word=word,
                note=initial_note,
            )
        else:
            processor = PROCESSORS_MAP.get(processor_name, None)  # type: ignore
            if processor is None:
                return None
            updated_note: CustomNote | None = processor.get_note_data(
                word=word,
                note=initial_note,
            )

        return updated_note

    def _get_content_using_multiple_processors(
        self,
        word: str,
        note: CustomNote,
    ) -> CustomNote | None:
        content: dict[str, Any] = {}
        updated_note = note
        for processor in PROCESSORS_MAP.values():
            if processor.__class__.__name__ == "OllamaDataProcessor":
                logger.info(msg=f"Skipping {processor.__class__.__name__} processor.")
                continue
            if processor.__class__.__name__ == "VerbenDataProcessor":
                # TODO: Change VerbenDataProcessor to use CustomFields
                logger.info(msg=f"Skipping {processor.__class__.__name__} processor.")
                continue

            updated_note: CustomNote | None = processor.get_note_data(
                word=word, note=note
            )

            if processor.is_content_complete(content=content):
                break

        return updated_note
