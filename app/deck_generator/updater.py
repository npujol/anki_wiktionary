import logging
from pathlib import Path
from typing import Any

from anki.collection import Collection, ImportAnkiPackageRequest
from anki.notes import Note

from .markdown_to_json import markdown_to_model_content
from .models import BasicModel, BasicModelContent


class AnkiDeckUpdater:
    def __init__(self, content_path: Path, deck_name: str, deck_path: Path) -> None:
        self.content_path: Path = content_path
        self.deck_name: str = deck_name
        self.deck_path: Path = deck_path
        new_path: Path = self.deck_path.parent / "collection.anki2"
        self.deck = Collection(path=str(new_path))
        self.deck_id: int = self.deck.decks.current()["id"]
        request = ImportAnkiPackageRequest()

        # Set the required fields (depends on the actual .proto structure)
        request.package_path = str(
            object=deck_path
        )  # Example: Set the path of the .apkg file

        self.deck.import_anki_package(request)

        self.logger: logging.Logger = logging.getLogger(name=__name__)

        model: dict[str, Any] | None = self.deck.models.by_name(name=self.deck_name)

        if model is not None:
            self.deck.models.remove(id=model["id"])

        self.deck.models.add(
            notetype=BasicModel(name=self.deck_name).to_anki_model(
                col=self.deck, model_name=self.deck_name
            )
        )

        self.model: dict[str, Any] | None = self.deck.models.by_name(
            name=self.deck_name
        )

    def process_markdown_files(self) -> None:
        """Processes all markdown files and adds notes to the deck."""

        notes: list[BasicModelContent] = markdown_to_model_content(
            content_path=self.content_path
        )

        for content_note in notes:
            new: dict[str, Any] = content_note.model_dump(mode="json")
            if not self.model:
                self.logger.warning(msg="Model not found.")
                continue
            new["id"] = self.model["id"]
            my_note: Note = self.deck.new_note(new)
            self.logger.debug(msg=f"Adding note: {my_note}")

    def run(self) -> str:
        """Runs the complete process of deck creation and export."""

        self.logger.info(msg=f"Folder path: {self.content_path}")
        self.logger.info(msg=f"Deck name: {self.deck_name}")

        self.process_markdown_files()
        self.deck.save()

        return str(self.deck_path)
