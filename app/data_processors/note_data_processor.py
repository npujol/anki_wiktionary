import logging
from typing import Optional

from app.data_processors import PROCESSORS_MAP
from app.serializers import CustomNote

logger = logging.getLogger(name=__name__)


class NoteDataProcessor:
    def __init__(
        self,
        deck_name: str = "Test",
        model_name: str = "Basic_",
    ) -> None:
        self.deck_name = deck_name
        self.model_name = model_name

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
