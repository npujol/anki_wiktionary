from typing import Any

import pytest

from app.data_processors.processors.wiktionary_data_processor import (
    WiktionaryDataProcessor,
)


@pytest.mark.vcr()
def test_get_wiktionary_data(snapshot: Any) -> None:
    result: dict[str, Any] = WiktionaryDataProcessor().get_note_data(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result, "The result does not match the snapshot"
