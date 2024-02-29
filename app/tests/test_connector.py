from app.connector import AnkiConnector
from app.serializers import Note
import pytest


@pytest.mark.vcr()
def test_add_note(
    anki_connector: AnkiConnector,
    note_obj: Note,
):
    result = anki_connector.add_note(note_obj)
    assert result, "Add note failed"


@pytest.mark.vcr()
def test_add_note_allow_duplicated(
    anki_connector: AnkiConnector,
    note_obj: Note,
):
    result = anki_connector.add_note(note_obj)
    assert result, "Add note failed"

    result = anki_connector.add_note(note_obj)
    assert result
