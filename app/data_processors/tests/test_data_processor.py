from typing import Any

import pytest

from app.data_processors.processor import NoteDataProcessor
from app.serializers import CustomNote


@pytest.mark.vcr()
def test_get_anki_note(snapshot: Any) -> None:
    result: CustomNote | None = NoteDataProcessor().get_anki_note(
        word="Abend", processor_name="wiktionary"
    )
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
    ],
)
def test_send_card_using_anki_web(
    processor_name: str,
    snapshot: Any,
) -> None:
    note: CustomNote | None = NoteDataProcessor(
        deck_name="deck_name",
        model_name="model_name",
    ).get_anki_note(
        word="Abend",
        processor_name=processor_name,
    )

    assert note, "Add note failed"
    assert snapshot("json") == note.model_dump(mode="python", by_alias=True)


@pytest.mark.vcr(mode="once")
def test_get_anki_note_without_processor_name(
    snapshot: Any,
) -> None:
    note: CustomNote | None = NoteDataProcessor(
        deck_name="deck_name",
        model_name="model_name",
    ).get_anki_note(
        word="Abend",
    )

    assert note, "Add note failed"
    assert snapshot("json") == note.model_dump(mode="python", by_alias=True)
