from pathlib import Path
from typing import Any

import pytest

from app.serializers import CustomFields, CustomNote


def test_custom_note_pretty_print(
    custom_note_obj: CustomNote,
    snapshot: Any,
) -> None:
    assert (
        snapshot("json") == custom_note_obj.pretty_print()
    ), "The result does not match the snapshot."


def test_import_from_content() -> None:
    initial_note = CustomNote(
        deckName="Test",
        modelName="Basic_",
        tags=[],
        audio=[],
        picture=[],
    )
    assert not initial_note.fields, "The result does not match the snapshot"
    content: dict[str, str] = {"full_word": "John Doe"}

    initial_note.import_from_content(content=content, fields_class=CustomFields)
    assert initial_note.fields, "The result does not match the snapshot"
    assert initial_note.fields.full_word == "John Doe"


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_add_audio_local(custom_note_obj: CustomNote) -> None:
    note: CustomNote = await custom_note_obj.add_audio()
    assert note, "Add note failed"
    assert note.audio, "The audio field is not set."

    path: Path = Path(custom_note_obj.audio[0].url)
    assert path.exists(), "The audio file was not generated."
    assert path.suffix == ".mp3", "The file is not an mp3."

    path.unlink()
