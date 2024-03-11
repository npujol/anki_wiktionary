import mwparserfromhell
from mwparserfromhell.nodes.tag import Tag
from mwparserfromhell.wikicode import Wikicode
from mwparserfromhell.nodes.wikilink import Wikilink
from wiktionary_de_parser.parser import Parser


ParseMeaningResult = list[str] | None


class ParseMeaning(Parser):
    name = "meaning"

    @staticmethod
    def parse_strings(parsed_paragraph: Wikicode):
        """
        Reference: https://de.wiktionary.org/wiki/Hilfe:Aussprache
        """
        found: list[str] = []
        sentence = ""
        for node in parsed_paragraph.nodes:
            # breakpoint()
            if node == ":":
                continue
            # allow "<ref>"-tags to follow
            if isinstance(node, Wikilink):
                # breakpoint()
                sentence += str(node.title) or ""
                continue
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
        # breakpoint()
        if found:
            return found

    @classmethod
    def parse(cls, wikitext: str):
        parsed_paragraph = mwparserfromhell.parse(wikitext)
        result = None
        # breakpoint()
        if parsed_paragraph:
            example = cls.parse_strings(parsed_paragraph)
            if example:
                result = example

        return result

    def run(self) -> ParseMeaningResult:
        # TODO Add support for "Beispiele"-templates
        paragraph = self.find_paragraph("Bedeutungen", self.entry.wikitext)
        result = None
        # breakpoint()
        if paragraph:
            result = self.parse(paragraph)
        return result
