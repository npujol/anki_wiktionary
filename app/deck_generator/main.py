import logging
import sys
from pathlib import Path

from app.deck_generator.updater import AnkiDeckUpdater

from .generator import AnkiDeckCreator

logger: logging.Logger = logging.getLogger(name=__name__)


def generate_deck(content_path: Path, deck_name: str) -> None:
    try:
        handler = AnkiDeckCreator(content_path=content_path, deck_name=deck_name)
        out: str = handler.run()
        logger.info(msg=f"Deck exported to: {out}")
    except Exception as e:
        logger.error(msg=f"Error while generating deck {deck_name}: {e}")
        sys.exit(1)


def update_deck(content_path: Path, deck_path: Path) -> None:
    try:
        deck_name: str = Path(deck_path).stem
        handler = AnkiDeckUpdater(
            content_path=content_path, deck_name=deck_name, deck_path=deck_path
        )
        out: str = handler.run()
        logger.info(msg=f"Deck exported to: {out}")
    except Exception as e:
        logger.error(
            msg=f"Error while updating deck {deck_name}, path: {deck_path} due to {e}"
        )
        sys.exit(1)
