import logging
from abc import ABC, abstractmethod
from typing import Any

from app.serializers import CustomNote


class BaseDataProcessor(ABC):
    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(name=__name__)

    def is_content_complete(self, content: dict[str, Any]) -> bool:
        """Return whether all required, non-translation fields have content."""
        fields_class = getattr(self, "fields_class", None)
        if fields_class is None:
            return False

        required_fields = (
            "full_word",
            "plural",
            "characteristics",
            "ipa",
            "meaning",
            "example1",
            "example2",
        )
        return all(content.get(field) for field in required_fields)

    @abstractmethod
    def get_note_data(self, word: str, note: CustomNote) -> CustomNote | None:
        pass

    @abstractmethod
    def _extract_from_content(self, word: str, content: Any) -> dict[str, Any]:
        pass
