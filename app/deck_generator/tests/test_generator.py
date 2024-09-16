import os
from pathlib import Path

from app.deck_generator.generator import AnkiDeckCreator
from app.helpers import to_valid_filename


def test_anki_deck_creator(temp_markdown_file: Path) -> None:
    """Test AnkiDeckCreator class functionality."""
    deck_name = "TestDeck"
    content_path: Path = temp_markdown_file.parent

    creator = AnkiDeckCreator(content_path=str(content_path), deck_name=deck_name)

    out: str = creator.run()

    deck_filename: str = f"{to_valid_filename(input=deck_name)}.apkg"
    output_path = Path(deck_filename)

    assert out == deck_filename, f"{out} != {deck_filename}"
    assert output_path.exists(), f"{deck_filename} was not created."

    if output_path.exists():
        os.remove(path=output_path)  # Remove the generated .apkg file
