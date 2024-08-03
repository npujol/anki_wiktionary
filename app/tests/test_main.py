import asyncio
from typing import Any

import pytest

from app.main import generate_note, get_anki_note_data


@pytest.mark.vcr()
def test_generate_notes_is_successful(snapshot: Any) -> None:
    result = generate_note(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result, "The result does not match the snapshot"


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_get_anki_note_data_is_successful(
    snapshot: Any,
) -> None:
    result = await asyncio.create_task(get_anki_note_data(word="Abend"))
    assert result, "Add note failed"
    assert snapshot("json") == result.model_dump(mode="python", by_alias=True)
