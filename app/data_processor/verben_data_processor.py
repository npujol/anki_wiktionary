import logging
from typing import Any

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(name=__name__)


class VerbenDataProcessor:
    def __init__(self) -> None:
        self.base_url = "https://www.verben.de/?w="

    def get_note_data(self, word: str) -> dict[str, Any]:
        response = requests.get(
            url=self.base_url + word,
        )

        if response.status_code != 200:
            logger.info(f"The request to {self.base_url} failed.")
            return {
                "Front": word,
                "Back": "",
            }
        # Get the content of the response
        page_content = response.content

        soup = BeautifulSoup(
            markup=page_content,
            features="html.parser",
        )
        body = soup.body
        body = soup.find("body")
        if body is None:
            return {
                "Front": word,
                "Back": "",
            }
        for script in body.find_all(["script", "style"]):
            script.decompose()

        return {
            "Front": word,
            "Back": str(body),
        }
