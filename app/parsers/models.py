from wiktionary_de_parser.models import ParsedWiktionaryPageEntry  # type: ignore

from .wiktionary.parser_examples import ParseExampleResult
from .wiktionary.parser_meaning import ParseMeaningResult


class CustomParsedWiktionaryPageEntry(ParsedWiktionaryPageEntry):
    example: ParseExampleResult
    meaning: ParseMeaningResult
