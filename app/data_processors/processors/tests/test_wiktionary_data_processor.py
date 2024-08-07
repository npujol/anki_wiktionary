from typing import Any

import pytest

from app.data_processors.processors.wiktionary_data_processor import (
    WiktionaryDataProcessor,
)
from app.serializers import CustomNote


@pytest.mark.vcr()
def test_get_wiktionary_data(initial_note: CustomNote, snapshot: Any) -> None:
    result: CustomNote | None = WiktionaryDataProcessor().get_note_data(
        word="Abend", note=initial_note
    )
    assert result, "Add note failed"
    assert result.fields, "The result does not match the snapshot"
    assert snapshot("json") == result.fields.model_dump(
        mode="python"
    ), "The result does not match the snapshot"
