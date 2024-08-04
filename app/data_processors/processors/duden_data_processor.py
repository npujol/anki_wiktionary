import logging
from typing import Any

import duden  # type: ignore
from duden.word import DudenWord  # type: ignore

from app.parsers.duden_parser import CustomDudenParser
from app.serializers import CustomFields

logger: logging.Logger = logging.getLogger(name=__name__)


# https://github.com/radomirbosak/duden
class DudenDataProcessor:
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
        content: None | DudenWord = duden.get(word=word)  # type: ignore
        if not content:
            logger.error(msg=f"Could not fetch data for word '{word}' using Duden.")
            return {
                "full_word": word,
            }

        content_dict: dict[str, Any] = self._extract_from_content(
            word=word, content=content
        )
        return content_dict

    def _extract_from_content(self, word: str, content: DudenWord) -> dict[str, Any]:
        parser = CustomDudenParser(duden_word=content)
        return {
            "full_word": word,
            "plural": parser.plural,
            "characteristics": parser.characteristics,
            "ipa": parser.ipa,
            "meaning": parser.meaning,
            "example1": parser.example1,
            "example2": parser.example2,
        }
