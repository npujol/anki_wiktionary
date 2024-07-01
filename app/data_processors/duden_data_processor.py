import logging
from typing import Any, Union

import duden
from duden.word import DudenWord

from app.parsers.duden_parser import CustomDudenParser
from app.serializers import CustomFields

logger = logging.getLogger(name=__name__)


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
        content = duden.get(word=word)
        if not content:
            return {
                "full_word": word,
            }

        content_dict = self._extract_from_content(word=word, content=content)
        return content_dict

    def _extract_from_content(self, word: str, content: DudenWord) -> dict[str, Any]:
        if not content:
            return {
                "full_word": word,
            }

        parser = CustomDudenParser(duden_word=content)
        return {
            "full_word": word,
            "plural": self._clean_content_field(content=content.grammar_overview),
            "characteristics": self._clean_content_field(content=content.part_of_speech)
            + "\n"
            + self._clean_content_field(content=content.usage),
            "ipa": self._clean_content_field(
                content=content.word_separation, separator="|"
            )
            + "\n"
            + self._clean_content_field(content=content.phonetic),
            "meaning": self._clean_content_field(content=content.meaning_overview)
            + "\n\n"
            + self._clean_content_field(content=content.synonyms),
            "example1": parser.example1,
            "example2": parser.example2,
        }

    def _clean_content_field(
        self, content: Union[str, list, None], separator: str = "\n"
    ) -> str:
        if isinstance(content, str):
            return content
        stack = [content]
        flat_list = []

        while stack:
            current = stack.pop()
            if isinstance(current, str):
                flat_list.append(current)
            elif isinstance(current, list):
                stack.extend(current[::-1])
        return separator.join(flat_list) if flat_list else ""
