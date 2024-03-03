from typing import Any
from app.data_processor import NoteDataProcessor, WiktionaryDataProcessor
import pytest


@pytest.mark.vcr()
def test_get_wiktionary_data(snapshot: Any):
    result = WiktionaryDataProcessor().get_wiktionary_data(word="Abend")
    assert result, "Add note failed"
    for key, value in enumerate(result):
        assert snapshot(f"{value.name}_{key}.json") == value.model_dump(
            mode="python", by_alias=True, exclude_none=True
        ), "The result does not match the snapshot"


@pytest.mark.vcr()
def test_get_anki_note(snapshot: Any):
    result = NoteDataProcessor().get_anki_note(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result.model_dump(
        mode="python", by_alias=True, exclude_none=True
    ), "The result does not match the snapshot"
