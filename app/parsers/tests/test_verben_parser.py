from typing import Any

import pytest
import requests
from bs4 import BeautifulSoup

from app.parsers.verben_parser import VerbenParser


@pytest.mark.vcr()
def test_custom_verben_parser(snapshot: Any) -> None:
    word = "Abend"
    response: requests.Response = requests.get(
        url="https://www.verben.de/?w=" + word,
    )

    # Get the content of the response
    page_content: bytes = response.content

    soup = BeautifulSoup(
        markup=page_content,
        features="html.parser",
    )
    parser: VerbenParser = VerbenParser(soup=soup)

    assert snapshot("json") == {
        "full_word": word,
        "plural": parser.plural,
        "characteristics": parser.characteristics,
        "ipa": parser.ipa,
        "meaning": parser.meaning,
        "example1": parser.example1,
        "example2": parser.example2,
    }
