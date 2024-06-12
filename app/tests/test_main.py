import asyncio
from typing import Any

import pytest

from app.data_processor.note_data_processor import NoteDataProcessor
from app.main import generate_note, get_anki_note_data


@pytest.mark.vcr()
def test_generate_notes(snapshot: Any):
    result = generate_note(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_get_anki_note_data(
    snapshot: Any,
):
    result = await asyncio.create_task(get_anki_note_data(word="Abend"))
    assert result, "Add note failed"
    assert snapshot("json") == result.model_dump(mode="python", by_alias=True)


@pytest.mark.vcr(mode="once")
@pytest.mark.parametrize(
    "processor_name",
    [
        "verben",
        "wiktionary",
        "ollama",
    ],
)
def test_send_card_using_anki_web(
    processor_name: str,
    snapshot: Any,
):
    note = NoteDataProcessor(
        deck_name="deck_name",
        model_name="model_name",
    ).get_anki_note(
        word="Abend",
        processor_name=processor_name,
    )

    assert note, "Add note failed"
    assert snapshot("json") == note.model_dump(mode="python", by_alias=True)
