from app.data_processor.ollama_data_processor import OllamaDataProcessor
from app.data_processor.verben_data_processor import VerbenDataProcessor
from app.data_processor.wiktionary_data_processor import WiktionaryDataProcessor

PROCESSORS_MAP = {
    "wiktionary": WiktionaryDataProcessor(),
    "ollama": OllamaDataProcessor(),
    "verben": VerbenDataProcessor(),
}
