import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(name=__name__)


class VerbenDataProcessor:
    def __init__(self) -> None:
        self.base_url = "https://www.verben.de/?w="

    def get_data(self, word: str) -> str:
        response = requests.get(
            url=self.base_url + word,
        )

        if response.status_code != 200:
            logger.info(f"The request to {self.base_url} failed.")
            return word
        # Get the content of the response
        page_content = response.content

        soup = BeautifulSoup(
            markup=page_content,
            features="html.parser",
        )
        body = soup.body
        body = soup.find("body")
        if body is None:
            return word
        for script in body.find_all(["script", "style"]):
            script.decompose()

        return str(body)
