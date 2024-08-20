from typing import Any

import duden  # type: ignore
import pytest
from duden.word import DudenWord  # type: ignore

from app.parsers.duden_parser import CustomDudenParser


@pytest.mark.vcr()
def test_custom_duden_parser(snapshot: Any) -> None:
    word = "Abend"
    content: None | DudenWord = duden.get(word=word, cache=False)  # type: ignore
    assert content is not None, "Could not fetch data for word 'Abend' using Duden."
    parser: CustomDudenParser = CustomDudenParser(duden_word=content)
    assert (
        parser.duden_word is not None
    ), "Could not fetch data for word 'Abend' using Duden."

    assert snapshot("json") == {
        "full_word": word,
        "plural": parser.plural,
        "characteristics": parser.characteristics,
        "ipa": parser.ipa,
        "meaning": parser.meaning,
        "example1": parser.example1,
        "example2": parser.example2,
    }
