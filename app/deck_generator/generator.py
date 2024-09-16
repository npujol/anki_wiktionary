import logging
import random
import sys
from pathlib import Path

import genanki

from app.helpers import to_valid_filename

logger: logging.Logger = logging.getLogger(name=__name__)


class AnkiDeckCreator:
    def __init__(self, content_path: str, deck_name: str) -> None:
        self.content_path = Path(content_path)
        self.deck_name: str = deck_name
        self.logger: logging.Logger = logging.getLogger(name=__name__)

    @staticmethod
    def generate_random_id() -> int:
        """Generates a random 10-digit ID."""
        return random.randint(1000000000, 9999999999)

    def create_deck(self) -> None:
        """Creates an Anki deck and model."""
        self.my_deck = genanki.Deck(
            deck_id=self.generate_random_id(), name=self.deck_name
        )
        self.my_model = genanki.Model(
            model_id=self.generate_random_id(),
            name="Simple Model",
            fields=[
                {"name": "front"},
                {"name": "back"},
            ],
            templates=[
                {
                    "name": "Card 1",
                    "qfmt": "{{front}}",
                    "afmt": '{{front}}<hr id="answer">{{back}}',
                },
            ],
        )

    def validate_content_path(self) -> None:
        """Checks if the provided content path exists."""
        if not self.content_path.exists():
            raise FileNotFoundError(f"Content path {self.content_path} does not exist.")

    def process_markdown_files(self) -> None:
        """Processes all markdown files and adds notes to the deck."""
        for file in self.content_path.glob(pattern="*.md"):
            with open(file=file, mode="r") as f:
                text_data: str = f.read()

            # Split text into sections
            sections: list[str] = text_data.strip().split(sep="##")

            # Loop through each section and extract front and back
            for section in sections:
                lines: list[str] = section.strip().split(sep="\n")
                subtitle: str = lines[0].replace("#", "").strip()  # Extract subtitle
                examples: list[str] = [
                    line.strip() for line in lines[1:] if line.strip()
                ]  # Extract examples

                if subtitle == "---":
                    continue  # Skip tags section
                if not examples:
                    continue  # Skip empty sections

                my_note = genanki.Note(
                    model=self.my_model,
                    fields=[subtitle, "\n".join(examples)],
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
