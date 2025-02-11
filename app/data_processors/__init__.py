from .processor import NoteDataProcessor  # type: ignore # noqa: F401
from .processors.base_data_processor import BaseDataProcessor  # type: ignore
from .processors.duden_data_processor import DudenDataProcessor  # type: ignore
from .processors.gemini_data_processor import GeminiDataProcessor  # type: ignore
from .processors.ollama_data_processor import OllamaDataProcessor  # type: ignore
from .processors.verben_data_processor import VerbenDataProcessor  # type: ignore
from .processors.wiktionary_data_processor import (
    WiktionaryDataProcessor,  # type: ignore
)

__all__ = [
    "BaseDataProcessor",
    "DudenDataProcessor",
    "OllamaDataProcessor",
    "VerbenDataProcessor",
    "WiktionaryDataProcessor",
    "GeminiDataProcessor",
]
