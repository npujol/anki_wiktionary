from typing import Any

import pytest

from app.data_processors import WiktionaryDataProcessor
from app.serializers import CustomNote


@pytest.mark.vcr()
@pytest.mark.parametrize(
    "word",
    [
        "Abend",
        "locker",
        "Bammel",
        "verstehen",
    ],
)
def test_get_wiktionary_data(
    word: str, initial_note: CustomNote, snapshot: Any
) -> None:
    result: CustomNote | None = WiktionaryDataProcessor().get_note_data(
        word=word, note=initial_note
    )
    assert result, "Add note failed"
    assert result.fields, "The result fields are empty"
    assert snapshot(f"{word}.json") == result.fields.model_dump(
        mode="python"
    ), "The result does not match the snapshot"
