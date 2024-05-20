import logging

import requests
from wiktionary_de_parser.models import WiktionaryPage

from app.parser.models import CustomParsedWiktionaryPageEntry
from app.parser.parser import CustomParser
from app.serializers import CustomFields, CustomNote

logger = logging.getLogger(name=__name__)


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

        content = requests.get(url=self.base_url, params=params).json().get("parse")

        if not content:
            return []

        parser = CustomParser()
        page = WiktionaryPage(
            page_id=content.get("pageid"),
            name=content.get("title"),
            wikitext=content.get("wikitext").get("*"),
        )
        word_types = []
        for entry in parser.entries_from_page(page=page):
            results = parser.custom_parse_entry(wiktionary_entry=entry)
            word_types.append(results)
        return word_types


class NoteDataProcessor:
    def __init__(self, deck_name: str = "Test", model_name: str = "Basic_") -> None:
        self.data_handler = WiktionaryDataProcessor()
        self.deck_name = deck_name
        self.model_name = model_name

    def get_anki_note(self, word: str) -> CustomNote | None:
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
