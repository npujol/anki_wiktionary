from typing import Any

import pytest

from app.data_processors.processor import NoteDataProcessor


@pytest.mark.vcr()
def test_get_anki_note(snapshot: Any) -> None:
    result = NoteDataProcessor().get_anki_note(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result.model_dump(
        mode="python", by_alias=True, exclude_none=True
    ), "The result does not match the snapshot"


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
) -> None:
    note = NoteDataProcessor(
        deck_name="deck_name",
        model_name="model_name",
    ).get_anki_note(
        word="Abend",
        processor_name=processor_name,
    )

    assert note, "Add note failed"
    assert snapshot("json") == note.model_dump(mode="python", by_alias=True)
