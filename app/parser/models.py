from wiktionary_de_parser.models import ParsedWiktionaryPageEntry

from app.parser.new_parser.parser_examples import ParseExampleResult
from app.parser.new_parser.parser_meaning import ParseMeaningResult


class CustomParsedWiktionaryPageEntry(ParsedWiktionaryPageEntry):
    example: ParseExampleResult
    meaning: ParseMeaningResult
