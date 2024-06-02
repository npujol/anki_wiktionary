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
            fields=CustomFields(
                full_word=word,
                plural=(
                    "\n    ".join(
                        f"{k}: {v}"
                        for k, v in content[0].flexion.items()
                        if "plural" in k.lower()
                    )
                    if content[0].flexion and content[0].flexion != ""
                    else ""
                ),
                characteristics=(
                    "\n    ".join(f"{k}: {v}" for k, v in content[0].flexion.items())
                    if content[0].flexion and content[0].flexion != ""
                    else ""
                ),
                ipa=", ".join(content[0].ipa or []),  # type: ignore
                meaning="\n    ".join(
                    c.strip().replace("\n", "")
                    for c in (content[0].meaning or [])
                    if c != "" and c.strip().replace("\n", "") != ""
                ),
                example1=content[0].example[0].strip().replace("\n", "")  # type: ignore
                if len(content) and len(content[0].example)  # type: ignore
                else "",
                example2=content[0].example[1].strip().replace("\n", "")  # type: ignore
                if len(content) and len(content[0].example) > 1  # type: ignore
                else "",  # type: ignore
            ),
            tags=["test"],
            audio=[],
            video=[],
            picture=[],
        )

        return note
