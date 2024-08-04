import logging
from typing import Any

import requests

from app.parsers.wiktionary_parser import CustomWiktionaryParser
from app.serializers import CustomFields

logger: logging.Logger = logging.getLogger(name=__name__)


class WiktionaryDataProcessor:
    def __init__(self) -> None:
        self.base_url = "https://de.wiktionary.org/w/api.php"
        self.fields_class = CustomFields

    def get_note_data(self, word: str) -> dict[str, Any]:
        """
        Fetches data from Wiktionary for a given word and returns a list of
        ParsedWiktionaryPageEntry objects.

        Args:
            word (str): The word to fetch data for.

        Returns:
            dict[str, Any]: A dictionary containing the fetched data.
        """
        params: dict[str, str] = {
            "action": "parse",
            "page": word,
            "prop": "wikitext",
            "format": "json",
        }

        content: Any = (
            requests.get(
                url=self.base_url,
                params=params,
            )
            .json()
            .get("parse")
        )

        if not content:
            logger.error(
                msg=f"Could not fetch data for word '{word}' using Wiktionary."
            )
            return {
                "full_word": word,
            }

        content_dict: dict[str, Any] = self._extract_from_content(
            word=word, content=content
        )
        return content_dict

    # TODO Move this to a base class
    def _extract_from_content(
        self, word: str, content: dict[str, Any]
    ) -> dict[str, Any]:
        parser = CustomWiktionaryParser(content=content)
        return {
            "full_word": word,
            "plural": parser.plural,
            "characteristics": parser.characteristics,
            "ipa": parser.ipa,
            "meaning": parser.meaning,
            "example1": parser.example1,
            "example2": parser.example2,
        }
