from typing import Any

import pytest

from app.anki_connectors.anki_local_connector import AnkiLocalConnector
from app.anki_connectors.errors import CollectionNotFoundError
from app.serializers import CustomNote, Note


@pytest.mark.vcr()
def test_add_note(
    anki_connector: AnkiLocalConnector,
    note_obj: Note,
    snapshot: Any,
) -> None:
    result: dict[str, Any] | None = anki_connector.add_note(note=note_obj)

    assert result, "Add note failed"
    assert snapshot("json") == result, "The returned JSON does not match the snapshot"


@pytest.mark.vcr()
def test_add_note_allow_duplicated(
    anki_connector: AnkiLocalConnector,
    note_obj: Note,
    snapshot: Any,
) -> None:
    result: dict[str, Any] | None = anki_connector.add_note(note=note_obj)

    assert result, "Add note failed"

    result = anki_connector.add_note(note=note_obj)

    assert result, "Add note failed"
    assert snapshot("json") == result, "The returned JSON does not match the snapshot"


@pytest.mark.vcr()
def test_add_custom_note(
    anki_connector: AnkiLocalConnector,
    custom_note_obj: CustomNote,
    snapshot: Any,
) -> None:
    result: dict[str, Any] | None = anki_connector.add_note(note=custom_note_obj)

    assert result, "Add note failed"
    assert snapshot("json") == result, "The returned JSON does not match the snapshot"


@pytest.mark.vcr()
def test_add_custom_note_with_failed_connection(
    anki_connector: AnkiLocalConnector,
    custom_note_obj: CustomNote,
    snapshot: Any,
    caplog: Any,
) -> None:
    with pytest.raises(expected_exception=CollectionNotFoundError):
        anki_connector.add_note(note=custom_note_obj)

    assert snapshot("json") == caplog.records[0].message


@pytest.mark.vcr()
def test_get_available_decks(
    anki_connector: AnkiLocalConnector,
    snapshot: Any,
) -> None:
    result: dict[str, Any] | None = anki_connector.get_available_decks()

    assert result, "Get available decks failed"
    assert snapshot("json") == result, "The returned JSON does not match the snapshot"


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
    result: dict[str, Any] | None = anki_connector.get_cards_from_deck(
        deck_name=deck_name
    )

    assert (
        snapshot(f"{deck_name}.json") == result
    ), f"The returned JSON from {deck_name=} does not match the snapshot"


@pytest.mark.vcr()
def test_get_models_and_ids(
    anki_connector: AnkiLocalConnector,
    snapshot: Any,
) -> None:
    result: dict[str, Any] | None = anki_connector.get_models_and_ids()

    assert result, "Get models and ids failed"
    assert snapshot("json") == result
