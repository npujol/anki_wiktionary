from pathlib import Path

from app.deck_generator import AnkiDeckUpdater


def test_run(tmp_content_path: Path, tmp_deck_path: Path) -> None:
    """Test the full process of deck creation and export."""
    # Run the complete process
    anki_deck_updater = AnkiDeckUpdater(
        content_path=tmp_content_path, deck_name="TestDeck", deck_path=tmp_deck_path
    )
    result: str = anki_deck_updater.run()

    # Verify the result path matches the expected deck path
    assert result == str(tmp_deck_path), "Deck path does not match expected path"

    # Verify that the deck file exists after running the process
    assert Path(result).exists(), "Deck file was not created"
