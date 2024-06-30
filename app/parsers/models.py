from wiktionary_de_parser.models import ParsedWiktionaryPageEntry

from app.parsers.wiktionary.parser_examples import ParseExampleResult
from app.parsers.wiktionary.parser_meaning import ParseMeaningResult


class CustomParsedWiktionaryPageEntry(ParsedWiktionaryPageEntry):
    example: ParseExampleResult
    meaning: ParseMeaningResult
