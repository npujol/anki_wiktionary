import mwparserfromhell  # type: ignore
from mwparserfromhell.nodes.tag import Tag  # type: ignore
from mwparserfromhell.nodes.wikilink import Wikilink  # type: ignore
from mwparserfromhell.wikicode import Wikicode  # type: ignore
from wiktionary_de_parser.parser import Parser  # type: ignore

ParseMeaningResult = list[str] | None


class ParseMeaning(Parser):
    name = "meaning"

    @staticmethod
    def parse_strings(parsed_paragraph: Wikicode) -> list[str] | None:
        """
        Reference: https://de.wiktionary.org/wiki/Hilfe:Aussprache
        """
        found: list[str] = []
        sentence: str = ""
        for node in parsed_paragraph.nodes:  # type: ignore
            if node == ":":
                continue
            # allow "<ref>"-tags to follow
            if isinstance(node, Wikilink):
                sentence += str(node.title)  # type: ignore
                if "\n" in node.title:
                    found.append(sentence)  # type: ignore
                    sentence = ""
                continue
            if isinstance(node, Tag) and node.tag == "ref":
                continue
            if hasattr(node, "value"):  # type: ignore
                sentence += node.value  # type: ignore
                if "\n" in node.value:  # type: ignore
                    found.append(sentence)  # type: ignore
                    sentence = ""
            elif hasattr(node, "contents"):  # type: ignore
                sentence += str(node.contents)  # type: ignore
                if "\n" in node.contents:  # type: ignore
                    found.append(sentence)  # type: ignore
                    sentence = ""

        if sentence:
            found.append(sentence)  # type: ignore
        if found:
            return found

    @classmethod
    def parse(cls, wikitext: str) -> list[str] | None:
        parsed_paragraph: Wikicode = mwparserfromhell.parse(value=wikitext)
        result: list[str] | None = None
        if parsed_paragraph:
            meaning: list[str] | None = cls.parse_strings(
                parsed_paragraph=parsed_paragraph
            )
            if meaning:
                result = meaning
        return result

    def run(self) -> ParseMeaningResult:
        paragraph: str | None = self.find_paragraph(
            heading="Bedeutungen", wikitext=self.entry.wikitext
        )
        result = None
        if paragraph:
            result: list[str] | None = self.parse(wikitext=paragraph)
        return result
