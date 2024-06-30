from app.data_processors.duden_data_processor import DudenDataProcessor
from app.data_processors.ollama_data_processor import OllamaDataProcessor
from app.data_processors.verben_data_processor import VerbenDataProcessor
from app.data_processors.wiktionary_data_processor import WiktionaryDataProcessor

PROCESSORS_MAP = {
    "wiktionary": WiktionaryDataProcessor(),
    "ollama": OllamaDataProcessor(),
    "verben": VerbenDataProcessor(),
    "duden": DudenDataProcessor(),
}
