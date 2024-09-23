import logging
from pathlib import Path

from app.deck_generator.cleanup import cleanup

from .models import BasicModelContent

logger: logging.Logger = logging.getLogger(name=__name__)


def markdown_to_model_content(content_path: Path) -> list[BasicModelContent]:
    """Converts markdown files to json format."""
    result: list[BasicModelContent] = []

    if not content_path.exists():
        raise FileNotFoundError(f"Content path {content_path} does not exist.")

    if not content_path.is_dir():
        logger.info(msg="Converting single markdown file to json")
        result += _markdown_to_model_content(file=content_path)
    else:
        logger.info(msg="Converting multiple markdown files to json")
        count = 0
        for file in content_path.glob(pattern="*.md"):
            count += 1
            logger.info(msg=f"Converting markdown file #{count}: {file}")
            result += _markdown_to_model_content(file=file)

    logger.info(
        msg=f"Converted {count} markdown files to length {len(result)} json notes."
    )
    return list(result)


def _markdown_to_model_content(file: Path) -> list[BasicModelContent]:
    """Converts a single markdown file to json format."""
    result: list[BasicModelContent] = []

    with open(file=file, mode="r") as f:
        text_data: str = f.read()

    # Split text into sections
    sections: list[str] = text_data.strip().split(sep="##")

    # Loop through each section and extract front and back
    for section in sections:
        lines: list[str] = section.strip().split(sep="\n")

        subtitle: str = cleanup(lines[0].replace("#", ""))  # Extract subtitle
        if subtitle == "---":
            logger.info(msg="Skipping tags section")
            continue  # Skip tags section

        examples: list[str] = [
            cleanup(line) for line in lines[1:] if cleanup(line)
        ]  # Extract examples

        if not examples:
            logger.info(msg="Skipping empty section")
            continue  # Skip empty sections
        result.append(BasicModelContent(front=subtitle, back="<br><br>".join(examples)))

    return result
