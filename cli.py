import logging

import click

from app import generate_deck, update_deck

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logger: logging.Logger = logging.getLogger(name=__name__)


@click.group()
@click.option("--deck", default="Default", help="Name of the Anki deck.")
@click.option(
    "--collection", required=True, help="Path to the Anki collection file (.anki2)."
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
    deck_name = ctx.obj["deck"]
    collection_path = ctx.obj["collection"]

    generate_deck(
        content_path=collection_path,
        deck_name=deck_name,
    )
    click.echo(message=f"Generated deck: {deck_name}.")


@cli.command()
@click.pass_context
@click.argument("deck_path", type=click.Path(exists=True))
def update(ctx, deck_path):
    deck_name = ctx.obj["deck"]
    collection_path = ctx.obj["collection"]

    update_deck(
        content_path=collection_path,
        deck_path=deck_path,
    )
    click.echo(message=f'Updated deck"{deck_name}".')


if __name__ == "__main__":
    cli(obj={})
