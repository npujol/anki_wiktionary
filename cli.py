import logging
import sys
from pathlib import Path

import click

from app import generate_deck, update_deck

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logger: logging.Logger = logging.getLogger(name=__name__)


@click.group()
@click.option("--deck", required=True, help="Name of the Anki deck.", type=str)
@click.option(
    "--collection",
    required=True,
    help="Path to the Anki collection file (.anki2).",
    type=click.Path(exists=True),
)
@click.pass_context
def cli(ctx, deck, collection):
    """CLI for managing Anki notes."""
    ctx.ensure_object(dict)
    ctx.obj["deck"] = deck
    ctx.obj["collection"] = collection


@cli.command()
@click.pass_context
def generate(ctx):
    deck_name = ctx.obj.get("deck")
    collection = ctx.obj.get("collection")

    if not deck_name or not collection:
        click.echo(message="Please provide a deck name and a collection path.")
        sys.exit(1)

    collection_path = Path(collection)

    if not collection_path.exists():
        click.echo(message="Collection path does not exist.")
        sys.exit(1)

    logger.info(msg=f"Collection path: {collection_path}")

    generate_deck(
        content_path=collection_path,
        deck_name=deck_name,
    )

    click.echo(message=f"Generated deck: {deck_name}.")
    sys.exit(0)


@cli.command()
@click.pass_context
@click.argument("deck_path", type=click.Path(exists=True))
def update(ctx, deck_path):
    deck_name = ctx.obj["deck"]
    collection = ctx.obj["collection"]

    logger.info(msg=f"Deck path: {deck_path}")
    if not deck_name or not collection:
        click.echo(message="Please provide a deck name and a collection path.")
        sys.exit(1)

    collection_path = Path(collection)

    if not collection_path.exists():
        click.echo(message="Collection path does not exist.")
        sys.exit(1)

    update_deck(
        content_path=collection_path,
        deck_path=deck_path,
    )

    click.echo(message=f"Updated deck {deck_name}.")
    sys.exit(0)


if __name__ == "__main__":
    cli(obj={})
