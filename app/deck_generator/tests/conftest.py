import os
from pathlib import Path
from typing import Any, Generator

import pytest

from app.helpers import to_valid_filename

# Sample markdown content for testing
sample_markdown_content = """
# Sample Title

## First Section
This is the front of the card.
This is the back of the card.

## Second Section
Front of another card.
Back of another card.

## Third Section
### Subsection
This is the front of the card.
This is the back of the card.
### Another Subsection
"""


@pytest.fixture
def temp_markdown_file(tmp_path: Path) -> Path:
    """Create a temporary markdown file for testing."""
    file_path: Path = tmp_path / "test_content.md"
    with open(file=file_path, mode="w") as f:
        f.write(sample_markdown_content)
    return file_path


# Cleanup after the test if the test fails and the file isn't removed
@pytest.fixture(scope="function", autouse=True)
def cleanup_deck_file() -> Generator[None, Any, None]:
    """Remove the generated deck file if it still exists."""
    yield
    deck_name = "TestDeck"
    deck_filename: str = f"{to_valid_filename(input=deck_name)}.apkg"
    output_path = Path(deck_filename)
    if output_path.exists():
        os.remove(path=output_path)
