import logging

import requests
from wiktionary_de_parser.models import WiktionaryPage

from app.parser.models import CustomParsedWiktionaryPageEntry
from app.parser.parser import CustomParser

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

        content = (
            requests.get(
                url=self.base_url,
                params=params,
            )
            .json()
            .get("parse")
        )

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
