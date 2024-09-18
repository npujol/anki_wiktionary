import re
from typing import Callable


def strip_spaces(text: str) -> str:
    """Replace multiple spaces with a single space."""
    return text.strip()


def replace_with_italic(text: str) -> str:
    """Replace text enclosed in underscores or asterisks with italicized HTML."""
    return re.sub(pattern=r"[_*]([^_*]+)[_*]", repl=r"<i>\1</i>", string=text)


def replace_with_bold(text: str) -> str:
    """
    Replace text enclosed in double underscores or double asterisks with bold HTML.
    """
    return re.sub(pattern=r"([*_]{2})([^*_]+)\1", repl=r"<b>\2</b>", string=text)


def cleanup_pipeline(s: str, steps: list) -> str:
    """Apply a sequence of functions to clean up a string."""
    for step in steps:
        s = step(s)
    return s


def cleanup(s: str) -> str:
    """Clean up a string."""
    steps: list[Callable[..., str]] = [
        strip_spaces,
        replace_with_bold,
        replace_with_italic,
    ]
    return cleanup_pipeline(s=s, steps=steps)
