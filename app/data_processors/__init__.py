from .processor import NoteDataProcessor
from .processors.base_data_processor import BaseDataProcessor
from .processors.duden_data_processor import DudenDataProcessor
from .processors.dwds_data_processor import DWDSDataProcessor
from .processors.gemini_data_processor import GeminiDataProcessor
from .processors.ollama_data_processor import OllamaDataProcessor
from .processors.verben_data_processor import VerbenDataProcessor
from .processors.wiktionary_data_processor import WiktionaryDataProcessor

__all__ = [
    "NoteDataProcessor",
    "BaseDataProcessor",
    "DWDSDataProcessor",
    "DudenDataProcessor",
    "OllamaDataProcessor",
    "VerbenDataProcessor",
    "WiktionaryDataProcessor",
    "GeminiDataProcessor",
]
