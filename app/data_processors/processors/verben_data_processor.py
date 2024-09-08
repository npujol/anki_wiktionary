import logging
from typing import Any

import requests
from bs4 import BeautifulSoup

from app.data_processors.processors.base_data_processor import BaseDataProcessor
from app.parsers.verben_parser import VerbenParser
from app.serializers import CustomFields, CustomNote

logger: logging.Logger = logging.getLogger(name=__name__)


# TODO Add a Custom Processor to handle Verben data
class VerbenDataProcessor(BaseDataProcessor):
    def __init__(self) -> None:
        self.base_url = "https://www.verben.de/?w="
        self.fields_class = CustomFields

    def get_note_data(self, word: str, note: CustomNote) -> CustomNote | None:
        response: requests.Response = requests.get(
            url=self.base_url + word,
        )

        if response.status_code != 200:
            logger.info(msg=f"The request to {self.base_url} failed.")
            return note
        # Get the content of the response
        page_content: bytes = response.content

        content = BeautifulSoup(
            markup=page_content,
            features="html.parser",
        )

        if not content:
            logger.error(msg=f"Could not fetch data for word '{word}' using Duden.")
            return note

        content_dict: dict[str, Any] = self._extract_from_content(
            word=word, content=content
        )
        updated_note: CustomNote | None = note.import_from_content(
            content=content_dict, fields_class=self.fields_class
        )

        return updated_note

    def _extract_from_content(self, word: str, content: Any) -> dict[str, Any]:
        parser = VerbenParser(soup=content)
        return {
            "full_word": word,
            "plural": parser.plural,
            "characteristics": parser.characteristics,
            "ipa": parser.ipa,
            "meaning": parser.meaning,
            "example1": parser.example1,
            "example2": parser.example2,
        }

    # def is_content_complete(self, content: dict[str, Any]) -> bool:
    #     # TODO: Review this and move to a base class
    #     return False
