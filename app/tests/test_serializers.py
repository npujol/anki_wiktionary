from typing import Any

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
        video=[],
        picture=[],
    )
    assert not initial_note.fields, "The result does not match the snapshot"
    content: dict[str, str] = {"full_word": "John Doe"}

    initial_note.import_from_content(content=content, fields_class=CustomFields)
    assert initial_note.fields, "The result does not match the snapshot"
    assert initial_note.fields.full_word == "John Doe"
