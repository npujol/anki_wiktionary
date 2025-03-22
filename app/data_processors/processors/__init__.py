from .base_data_processor import BaseDataProcessor  # type: ignore
from .duden_data_processor import DudenDataProcessor  # type: ignore
from .dwds_data_processor import DWDSDataProcessor
from .gemini_data_processor import GeminiDataProcessor  # type: ignore
from .ollama_data_processor import OllamaDataProcessor  # type: ignore
from .verben_data_processor import VerbenDataProcessor  # type: ignore
from .wiktionary_data_processor import WiktionaryDataProcessor  # type: ignore

__all__ = [
    "BaseDataProcessor",
    "DudenDataProcessor",
    "DWDSDataProcessor",
    "OllamaDataProcessor",
    "VerbenDataProcessor",
    "WiktionaryDataProcessor",
    "GeminiDataProcessor",
]
