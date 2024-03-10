from wiktionary_de_parser.models import ParsedWiktionaryPageEntry

from app.parser.new_parser.parser_examples import ParseExampleResult


class CustomParsedWiktionaryPageEntry(ParsedWiktionaryPageEntry):
    example: ParseExampleResult
