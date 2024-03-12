import mwparserfromhell
from mwparserfromhell.nodes.tag import Tag
from mwparserfromhell.wikicode import Wikicode

from wiktionary_de_parser.parser import Parser


ParseExampleResult = list[str] | None


class ParseExample(Parser):
    name = "example"

    @staticmethod
    def parse_strings(parsed_paragraph: Wikicode):
        """
        Reference: https://de.wiktionary.org/wiki/Hilfe:Beispiele
        """
        found: list[str] = []
        sentence = ""
        for node in parsed_paragraph.nodes:
            if node == ":":
                continue
            # allow "<ref>"-tags to follow
            if isinstance(node, Tag) and node.tag == "ref":
                continue
            if hasattr(node, "value"):
                if node.value.startswith("["):
                    sentence += node.value
                else:
                    sentence += node.value
                    found.append(sentence)
                    sentence = ""
            elif hasattr(node, "contents"):
                sentence += str(node.contents)

        if sentence:
            found.append(sentence)
        if found:
            return found

    @classmethod
    def parse(cls, wikitext: str):
        parsed_paragraph = mwparserfromhell.parse(wikitext)
        result = None
        if parsed_paragraph:
            example = cls.parse_strings(parsed_paragraph)
            if example:
                result = example

        return result

    def run(self) -> ParseExampleResult:
        paragraph = self.find_paragraph("Beispiele", self.entry.wikitext)
        result = None

        if paragraph:
            result = self.parse(paragraph)
        return result
