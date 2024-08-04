from wiktionary_de_parser.models import ParsedWiktionaryPageEntry  # type: ignore

from app.parsers.wiktionary.parser_examples import ParseExampleResult
from app.parsers.wiktionary.parser_meaning import ParseMeaningResult


class CustomParsedWiktionaryPageEntry(ParsedWiktionaryPageEntry):
    example: ParseExampleResult
    meaning: ParseMeaningResult
