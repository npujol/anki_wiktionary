import logging
from typing import Any

import requests
from wiktionary_de_parser.models import WiktionaryPage

from app.parser.models import CustomParsedWiktionaryPageEntry
from app.parser.parser import CustomParser

logger = logging.getLogger(name=__name__)


class WiktionaryDataProcessor:
    def __init__(self) -> None:
        self.base_url = "https://de.wiktionary.org/w/api.php"

    def get_wiktionary_data(self, word: str) -> dict[str, Any]:
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
            return {
                "full_word": word,
            }

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

        content_dict = self._extract_from_content(word=word, content=word_types)
        return content_dict

    def _extract_from_content(
        self, word: str, content: list[CustomParsedWiktionaryPageEntry]
    ):
        first = content[0]
        return {
            "full_word": word,
            "plural": (
                "\n    ".join(
                    f"{k}: {v}"
                    for k, v in first.flexion.items()
                    if "plural" in k.lower()
                )
                if first.flexion and first.flexion != ""
                else ""
            ),
            "characteristics": (
                "\n    ".join(f"{k}: {v}" for k, v in first.flexion.items())
                if first.flexion and first.flexion != ""
                else ""
            ),
            "ipa": ", ".join(first.ipa or []),
            "meaning": "\n    ".join(
                c.strip().replace("\n", "")
                for c in (first.meaning or [])
                if c != "" and c.strip().replace("\n", "") != ""
            ),
            "example1": first.example[0].strip().replace("\n", "")
            if first.example is not None and len(first.example)
            else "",
            "example2": first.example[1].strip().replace("\n", "")
            if first.example is not None and len(first.example) > 1
            else "",
        }
