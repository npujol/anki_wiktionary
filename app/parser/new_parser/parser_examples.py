import mwparserfromhell
from mwparserfromhell.nodes.tag import Tag
from mwparserfromhell.nodes.template import Template
from mwparserfromhell.nodes.text import Text
from mwparserfromhell.wikicode import Wikicode

from wiktionary_de_parser.parser import Parser

WANTED_TABLE_NAMES = [
    "Deutsch Adjektiv Übersicht",
    "Deutsch Adverb Übersicht",
    "Deutsch Eigenname Übersicht",
    "Deutsch Nachname Übersicht",
    "Deutsch Pronomen Übersicht",
    "Deutsch Substantiv Übersicht",
    "Deutsch Substantiv Übersicht -sch",
    "Deutsch adjektivisch Übersicht",
    "Deutsch Toponym Übersicht",
    "Deutsch Verb Übersicht",
]

ParseExampleResult = list[str] | None


class ParseExample(Parser):
    name = "Example"

    @staticmethod
    def parse_ipa_strings(parsed_paragraph: Wikicode):
        """
        Reference: https://de.wiktionary.org/wiki/Hilfe:Beispiele
        """

        found_ipa: list[str] = []
        found_ipa_tmpl = False

        for node in parsed_paragraph.nodes:
            # IPA-template must be present to start parsing Lautschrift-template
            if found_ipa_tmpl is False:
                if isinstance(node, Template) and node.name == "IPA":
                    found_ipa_tmpl = True

            # allow "Lautschrift"-templates to follow
            elif (
                isinstance(node, Template)
                and node.name == "Lautschrift"
                and node.params
            ):
                ipa_text = str(node.params[0]).replace("…", "").strip()

                if ipa_text and ipa_text not in found_ipa:
                    found_ipa.append(ipa_text)

            # allow commas between "Lautschrift"-template to follow
            elif isinstance(node, Text) and node.value == ", ":
                continue

            # allow "<ref>"-tags to follow
            elif isinstance(node, Tag) and node.tag == "ref":
                continue

            else:
                # skip if no IPA-string has been found yet
                if not found_ipa:
                    continue
                # break if another not supported node follows
                else:
                    break

        if found_ipa:
            return found_ipa

    @classmethod
    def parse(cls, wikitext: str):
        parsed_paragraph = mwparserfromhell.parse(wikitext)
        result = None

        return result

    def run(self) -> ParseExampleResult:
        # TODO Add support for "Beispiele"-templates
        paragraph = self.find_paragraph("Beispiele", self.entry.wikitext)
        result = None

        if paragraph:
            result = self.parse(paragraph)

        return result
