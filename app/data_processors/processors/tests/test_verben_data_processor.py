from typing import Any

import pytest

from app.data_processors import VerbenDataProcessor
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
def test_get_data_from_verben(
    word: str, initial_note: CustomNote, snapshot: Any
) -> None:
    result: CustomNote | None = VerbenDataProcessor().get_note_data(
        word=word, note=initial_note
    )
    assert result, "Add note failed"
    assert result.fields, "The result fields are empty"
    assert snapshot(f"{word}.json") == result.fields.model_dump(
        mode="python"
    ), "The result does not match the snapshot"
