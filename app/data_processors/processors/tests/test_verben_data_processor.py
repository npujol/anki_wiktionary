from typing import Any

import pytest

from app.data_processors.processors.verben_data_processor import VerbenDataProcessor
from app.serializers import CustomNote


@pytest.mark.vcr(mode="once")
def test_get_data_from_verben(initial_note: CustomNote, snapshot: Any) -> None:
    result: CustomNote | None = VerbenDataProcessor().get_note_data(
        word="Abend", note=initial_note
    )
    assert result, "Add note failed"
    assert result.fields, "The result does not match the snapshot"
    assert snapshot("json") == result.fields.model_dump(
        mode="python"
    ), "The result does not match the snapshot"
