from typing import Any

import pytest

from app.anki_connectors.anki_local_connector import AnkiLocalConnector
from app.serializers import CustomNote, Note


@pytest.mark.vcr()
def test_add_note(
    anki_connector: AnkiLocalConnector,
    note_obj: Note,
) -> None:
    result = anki_connector.add_note(note=note_obj)
    assert result, "Add note failed"


@pytest.mark.vcr()
def test_add_note_allow_duplicated(
    anki_connector: AnkiLocalConnector,
    note_obj: Note,
) -> None:
    result = anki_connector.add_note(note=note_obj)
    assert result, "Add note failed"

    result = anki_connector.add_note(note=note_obj)
    assert result


@pytest.mark.vcr()
def test_get_available_decks(
    anki_connector: AnkiLocalConnector,
    snapshot: Any,
) -> None:
    result = anki_connector.get_available_decks()
    assert snapshot("json") == result


@pytest.mark.vcr()
@pytest.mark.parametrize(
    "deck_name",
    [
        "Test",
        "Mein Deutsch",
        "Default",
    ],
)
def test_get_cards_from_deck(
    deck_name: str,
    anki_connector: AnkiLocalConnector,
    snapshot: Any,
) -> None:
    result = anki_connector.get_cards_from_deck(deck_name=deck_name)
    assert snapshot(f"{deck_name}.json") == result


@pytest.mark.vcr()
def test_add_custom_note(
    anki_connector: AnkiLocalConnector,
    custom_note_obj: CustomNote,
) -> None:
    result = anki_connector.add_note(note=custom_note_obj)
    assert result, "Add note failed"


@pytest.mark.vcr()
def test_get_models_and_ids(
    anki_connector: AnkiLocalConnector,
    snapshot: Any,
) -> None:
    result = anki_connector.get_models_and_ids()
    assert snapshot("json") == result
