import mwparserfromhell  # type: ignore
from mwparserfromhell.nodes.tag import Tag  # type: ignore
from mwparserfromhell.wikicode import Wikicode  # type: ignore
from wiktionary_de_parser.parser import Parser  # type: ignore

ParseExampleResult = list[str] | None


class ParseExample(Parser):
    name = "example"

    @staticmethod
    def parse_strings(parsed_paragraph: Wikicode) -> list[str] | None:
        """
        Reference: https://de.wiktionary.org/wiki/Hilfe:Beispiele
        """
        found: list[str] = []
        sentence: str = ""
        for node in parsed_paragraph.nodes:  # type: ignore
            if node == ":":
                continue
            # allow "<ref>"-tags to follow
            if isinstance(node, Tag) and node.tag == "ref":
                continue
            if hasattr(node, "value"):  # type: ignore
                if node.value.startswith("["):  # type: ignore
                    sentence += node.value  # type: ignore
                else:
                    sentence += node.value  # type: ignore
                    found.append(sentence)  # type: ignore
                    sentence = ""
            elif hasattr(node, "contents"):  # type: ignore
                sentence += str(node.contents)  # type: ignore

        if sentence:
            found.append(sentence)  # type: ignore
        if found:
            return found

    @classmethod
    def parse(cls, wikitext: str) -> list[str] | None:
        parsed_paragraph: Wikicode = mwparserfromhell.parse(value=wikitext)
        result: list[str] | None = None
        if parsed_paragraph:
            example: list[str] | None = cls.parse_strings(
                parsed_paragraph=parsed_paragraph
            )
            if example:
                result = example

        return result

    def run(self) -> ParseExampleResult:
        paragraph: str | None = self.find_paragraph(
            heading="Beispiele", wikitext=self.entry.wikitext
        )
        result = None

        if paragraph:
            result: list[str] | None = self.parse(wikitext=paragraph)
        return result
