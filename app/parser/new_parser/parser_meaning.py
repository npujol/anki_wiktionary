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
            if node == ":":
                continue
            # allow "<ref>"-tags to follow
            if isinstance(node, Wikilink):
                sentence += str(node.title)
                if "\n" in node.title:
                    found.append(sentence)
                    sentence = ""
                continue
            if isinstance(node, Tag) and node.tag == "ref":
                continue
            if hasattr(node, "value"):
                sentence += node.value
                if "\n" in node.value:
                    found.append(sentence)
                    sentence = ""
            elif hasattr(node, "contents"):
                sentence += str(node.contents)
                if "\n" in node.contents:
                    found.append(sentence)
                    sentence = ""

        if sentence:
            found.append(sentence)
        if found:
            return found

    @classmethod
    def parse(cls, wikitext: str):
        parsed_paragraph = mwparserfromhell.parse(wikitext)
        result = None
        if parsed_paragraph:
            meaning = cls.parse_strings(parsed_paragraph)
            if meaning:
                result = meaning
        return result

    def run(self) -> ParseMeaningResult:
        paragraph = self.find_paragraph("Bedeutungen", self.entry.wikitext)
        result = None
        if paragraph:
            result = self.parse(paragraph)
        return result
