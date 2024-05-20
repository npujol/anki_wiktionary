from typing import Any

import pytest

from app.data_processor import NoteDataProcessor, WiktionaryDataProcessor


@pytest.mark.vcr()
def test_get_wiktionary_data(snapshot: Any) -> None:
    result = WiktionaryDataProcessor().get_wiktionary_data(word="Abend")
    assert result, "Add note failed"
    for key, value in enumerate(iterable=result):
        assert snapshot(f"{value.name}_{key}.json") == value.model_dump(
            mode="python", by_alias=True, exclude_none=True
        ), "The result does not match the snapshot"


@pytest.mark.vcr()
def test_get_anki_note(snapshot: Any) -> None:
    result = NoteDataProcessor().get_anki_note(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result.model_dump(
        mode="python", by_alias=True, exclude_none=True
    ), "The result does not match the snapshot"
