def clean_text(text: str) -> str:
    """
    Remove soft hyphens anywhere, and heading and trailing spaces.
    """
    return text.replace("\xad", "").strip()
