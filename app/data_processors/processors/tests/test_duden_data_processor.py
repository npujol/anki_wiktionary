from typing import Any

import pytest

from app.data_processors.processors.duden_data_processor import DudenDataProcessor


@pytest.mark.vcr(mode="once")
@pytest.mark.parametrize(
    "word",
    [
        "Abend",
        "locker",
        "Bammel",
        "selbstverteidigung",
    ],
)
def test_get_data_from_duden(word: str, snapshot: Any) -> None:
    result = DudenDataProcessor().get_note_data(word=word)
    assert result, "Add note failed"
    assert snapshot(f"{word}.json") == result
