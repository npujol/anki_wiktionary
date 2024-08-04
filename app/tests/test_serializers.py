from typing import Any

from app.serializers import CustomNote


def test_custom_note_pretty_print(
    custom_note_obj: CustomNote,
    snapshot: Any,
) -> None:
    assert (
        snapshot("json") == custom_note_obj.pretty_print()
    ), "The result does not match the snapshot."
