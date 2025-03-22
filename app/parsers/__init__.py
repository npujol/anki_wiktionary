from .duden_parser import CustomDudenParser
from .dwds_parser import CustomDWDSParser
from .verben_parser import VerbenParser
from .wiktionary_parser import CustomWiktionaryParser

__all__: list[str] = [
    "CustomDWDSParser",
    "VerbenParser",
    "CustomWiktionaryParser",
    "CustomDudenParser",
]
