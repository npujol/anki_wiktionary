from abc import ABC, abstractmethod
from typing import Any


class BaseDataProcessor(ABC):
    def is_content_complete(self, content: dict[str, Any]) -> bool:
        # TODO: Review this and move to a base class
        return all(
            field in content and content.get(field)  # type: ignore
            for field in self.fields_class.__fields__  # type: ignore
        )

    @abstractmethod
    def get_note_data(self, word: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def _extract_from_content(self, word: str, content: Any) -> dict[str, Any]:
        pass
