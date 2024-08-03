from typing import Any

import pytest

from app.data_processors.processor import NoteDataProcessor


@pytest.mark.vcr()
def test_get_anki_note(snapshot: Any) -> None:
    result = NoteDataProcessor().get_anki_note(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result.model_dump(
        mode="python", by_alias=True, exclude_none=True
    ), "The result does not match the snapshot"
