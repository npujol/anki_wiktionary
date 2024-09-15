import re


def to_valid_filename(input: str) -> str:
    # Convert to lowercase, remove leading/trailing spaces, and replace non-alphanumeric
    # characters with dashes
    cleaned_string: str = re.sub(
        pattern=r"[^a-zA-Z0-9-]+", repl="-", string=input.lower().strip()
    )

    # Replace multiple consecutive dashes with a single dash, and remove any
    # leading/trailing dashes
    return re.sub(
        pattern=r"^-+|-+$",
        repl="",
        string=re.sub(pattern=r"-{2,}", repl="-", string=cleaned_string),
    )
