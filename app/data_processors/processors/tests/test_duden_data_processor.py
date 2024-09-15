from typing import Any

import pytest

from app.data_processors.processors.duden_data_processor import DudenDataProcessor
from app.serializers import CustomNote


@pytest.mark.vcr(mode="once")
@pytest.mark.parametrize(
    "word",
    [
        "Abend",
        "locker",
        "Bammel",
        "Verstehen",
        "verstehen",
    ],
)
def test_get_data_from_duden(
    word: str, initial_note: CustomNote, snapshot: Any
) -> None:
    result: CustomNote | None = DudenDataProcessor().get_note_data(
        word=word,
        note=initial_note,
    )
    assert result, "Add note failed"
    assert result.fields, "The result  fields are empty"
    assert snapshot("json") == result.fields.model_dump(
        mode="python"
    ), "The result does not match the snapshot"
