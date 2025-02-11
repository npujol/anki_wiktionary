import logging
from typing import Any, Optional

from app.serializers import CustomNote

from .processors import (
    BaseDataProcessor,
    DudenDataProcessor,
    GeminiDataProcessor,
    # OllamaDataProcessor,
    VerbenDataProcessor,
    WiktionaryDataProcessor,
)

PROCESSORS_MAP: dict[
    str,
    BaseDataProcessor,
] = {
    "verben": VerbenDataProcessor(),
    "duden": DudenDataProcessor(),
    "wiktionary": WiktionaryDataProcessor(),
    # "ollama": OllamaDataProcessor(),
    "gemini": GeminiDataProcessor(),
}


class NoteDataProcessor:
    def __init__(
        self,
        deck_name: str = "Test",
        model_name: str = "Basic_",
    ) -> None:
        self.deck_name: str = deck_name
        self.model_name: str = model_name
        self.logger: logging.Logger = logging.getLogger(name=__name__)

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
                self.logger.info(
                    msg=f"Skipping {processor.__class__.__name__} processor."
                )
                continue
            if processor.__class__.__name__ == "VerbenDataProcessor":
                # TODO: Change VerbenDataProcessor to use CustomFields
                self.logger.info(
                    msg=f"Skipping {processor.__class__.__name__} processor."
                )
                continue

            updated_note: CustomNote | None = processor.get_note_data(
                word=word, note=note
            )

            if processor.is_content_complete(content=content):
                break

        return updated_note
