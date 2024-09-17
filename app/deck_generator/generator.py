import logging
import sys
from pathlib import Path

import genanki

from app.deck_generator.helpers import generate_random_id
from app.deck_generator.markdown_to_json import markdown_to_json
from app.deck_generator.models import BasicModel, BasicModelContent
from app.helpers import to_valid_filename

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger: logging.Logger = logging.getLogger(name=__name__)


class AnkiDeckCreator:
    def __init__(self, content_path: str, deck_name: str) -> None:
        self.content_path = Path(content_path)
        self.deck_name: str = deck_name
        self.logger: logging.Logger = logging.getLogger(name=__name__)

    def create_deck(self) -> None:
        """Creates an Anki deck and model."""
        self.my_deck = genanki.Deck(deck_id=generate_random_id(), name=self.deck_name)
        self.my_model = BasicModel().to_genanki_model()

    def validate_content_path(self) -> None:
        """Checks if the provided content path exists."""
        if not self.content_path.exists():
            raise FileNotFoundError(f"Content path {self.content_path} does not exist.")

    def process_markdown_files(self) -> None:
        """Processes all markdown files and adds notes to the deck."""

        notes: list[BasicModelContent] = markdown_to_json(
            content_path=self.content_path
        )
        for content_note in notes:
            my_note = genanki.Note(
                model=self.my_model,
                fields=[content_note.front, content_note.back],
            )
            self.my_deck.add_note(note=my_note)

    def export_deck(self) -> str:
        """Exports the Anki deck to an .apkg file."""
        my_package = genanki.Package(deck_or_decks=self.my_deck)
        out: str = f"{to_valid_filename(input=self.deck_name)}.apkg"
        my_package.write_to_file(file=out)

        return out

    def run(self) -> str:
        """Runs the complete process of deck creation and export."""
        self.logger.info(msg=f"Folder path: {self.content_path}")
        self.logger.info(msg=f"Deck name: {self.deck_name}")

        self.validate_content_path()
        self.create_deck()
        self.process_markdown_files()

        return self.export_deck()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        content_path: str = sys.argv[1]
        deck_name: str = sys.argv[2]  # Extracts deck name from the folder path

        anki_creator = AnkiDeckCreator(content_path=content_path, deck_name=deck_name)
        try:
            out: str = anki_creator.run()
            logger.info(msg=f"Deck exported to: {out}")
        except Exception as e:
            logger.error(msg=f"Error while generating deck: {e}")
            sys.exit(1)
    else:
        logger.error(msg="No arguments provided.")
        sys.exit(1)
