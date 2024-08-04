class CollectionNotFoundError(Exception):
    """
    Raised when an Anki collection is not found.
    """


class ResultNotFoundError(Exception):
    """
    Raised when an Anki result is not found.
    """


class BrowserNotFoundError(Exception):
    """
    Raised when a browser is not found.
    """
