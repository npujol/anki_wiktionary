import logging
from typing import Any

import requests
from bs4 import BeautifulSoup

from app.html_processors import prune_html_tags
from app.serializers import BasicFields

logger = logging.getLogger(name=__name__)


# TODO Add a Custom Processor to handle Verben data
class VerbenDataProcessor:
    def __init__(self) -> None:
        self.base_url = "https://www.verben.de/?w="
        self.fields_class = BasicFields

    def get_note_data(self, word: str) -> dict[str, Any]:
        response = requests.get(
            url=self.base_url + word,
        )

        if response.status_code != 200:
            logger.info(msg=f"The request to {self.base_url} failed.")
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

        info_selector = "body > article > div:nth-child(1) > div.rAbschnitt"
        lateral_info_selector = "body > article > div:nth-child(1) > div.rInfo"

        # Find the elements using the CSS selectors
        info_element = soup.select_one(selector=info_selector)
        lateral_info_element = soup.select_one(selector=lateral_info_selector)

        body = (
            str(object=prune_html_tags(html=info_element))
            if info_element
            else "" + "<br>" + str(prune_html_tags(html=lateral_info_element))
            if lateral_info_element
            else ""
        )

        return {
            "Front": word,
            "Back": str(body),
        }
