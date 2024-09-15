import logging
from abc import ABC, abstractmethod
from typing import Any

from app.serializers import CustomNote


class BaseDataProcessor(ABC):
    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(name=__name__)

    def is_content_complete(self, content: dict[str, Any]) -> bool:
        return all(
            field in content and content.get(field)  # type: ignore
            for field in self.fields_class.model_fields  # type: ignore
        )

    @abstractmethod
    def get_note_data(self, word: str, note: CustomNote) -> CustomNote | None:
        pass

    @abstractmethod
    def _extract_from_content(self, word: str, content: Any) -> dict[str, Any]:
        pass
