import logging
import requests
from wiktionary_de_parser.models import WiktionaryPage
from app.parser.models import CustomParsedWiktionaryPageEntry
from app.parser.parser import CustomParser
from app.serializers import CustomFields, CustomNote

logger = logging.getLogger(__name__)


class WiktionaryDataProcessor:
    def __init__(self) -> None:
        self.base_url = "https://de.wiktionary.org/w/api.php"

    def get_wiktionary_data(self, word: str) -> list[CustomParsedWiktionaryPageEntry]:
        """
        Fetches data from Wiktionary for a given word and returns a list of
        ParsedWiktionaryPageEntry objects.

        Args:
            word (str): The word to fetch data for.

        Returns:
            list[ParsedWiktionaryPageEntry]: A list of ParsedWiktionaryPageEntry objects
            containing information about the word.
        """
        params = {
            "action": "parse",
            "page": word,
            "prop": "wikitext",
            "format": "json",
        }

        content = requests.get(self.base_url, params=params).json().get("parse")

        if not content:
            return []

        parser = CustomParser()
        page = WiktionaryPage(
            page_id=content.get("pageid"),
            name=content.get("title"),
            wikitext=content.get("wikitext").get("*"),
        )
        word_types = []
        for entry in parser.entries_from_page(page):
            results = parser.custom_parse_entry(entry)
            word_types.append(results)
        return word_types


class NoteDataProcessor:
    def __init__(self, deck_name: str = "Test", model_name: str = "Basic_") -> None:
        self.data_handler = WiktionaryDataProcessor()
        self.deck_name = deck_name
        self.model_name = model_name

    def get_anki_note(self, word: str) -> CustomNote | None:
        content = self.data_handler.get_wiktionary_data(word)
        if not content:
            logger.info(f"Note for {word} not found.")
            return
        if not content[0]:
            logger.info(f"Note for {word} not found.")
            return
        note = CustomNote(
            deckName=self.deck_name,
            modelName=self.model_name,
            fields=CustomFields(
                full_word=word,
                plural="|".join(
                    f"{k}: {v}"
                    for k, v in content[0].flexion.items()
                    if "plural" in k.lower()
                )
                if content[0].flexion
                else "",
                characteristics="|".join(
                    f"{k}: {v}" for k, v in content[0].flexion.items()
                )
                if content[0].flexion
                else "",
                ipa=",".join(content[0].ipa or []),  # type: ignore
                # audio=content[0].audio, TODO: Add audio support
                meaning="|".join(content[0].meaning or []),
                # meaning_spanish=content[0].meaning_spanish, TODO: Add meaning support
                example1=content[0].example[0] or "",  # type: ignore
                # example1e=content[0].example1e, TODO: Add example support
                example2=content[0].example[1] or "",  # type: ignore
                # example2e=content[0].example2e, TODO: Add example support
            ),
            tags=["test"],
            audio=[],
            video=[],
            picture=[],
        )

        return note
