from typing import Any

import pytest

from app.data_processors.processors.verben_data_processor import VerbenDataProcessor


@pytest.mark.vcr(mode="once")
def test_get_data_from_verben(snapshot: Any) -> None:
    result = VerbenDataProcessor().get_note_data(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result
