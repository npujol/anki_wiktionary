import importlib.util
import inspect
from pathlib import Path
from typing import Any

from wiktionary_de_parser import WiktionaryParser
from wiktionary_de_parser.models import WiktionaryPage, WiktionaryPageEntry
from wiktionary_de_parser.parser import Parser

from app.parsers.models import CustomParsedWiktionaryPageEntry


class CustomWiktionaryParser(WiktionaryParser):
    def __init__(self, content: dict[str, str], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        new_parsers = self.find_new_parser_classes()
        self.parser_classes = self.parser_classes + new_parsers
        self.word_types = self._extract_word_types(content=content)
        self.first_word = self.word_types[0] or None

    @staticmethod
    def find_new_parser_classes() -> list[Any]:
        path = Path(__file__).parent / "wiktionary"
        parent_class = Parser
        classes = []

        for child in path.iterdir():
            if (
                child.is_file()
                and child.name.endswith(".py")
                and child.name != "__init__.py"
            ):
                module_name = child.stem
                spec = importlib.util.spec_from_file_location(
                    name=module_name, location=child
                )

                if not spec or not spec.loader:
                    raise Exception(f"Could not load {child}")

                module = importlib.util.module_from_spec(spec=spec)
                spec.loader.exec_module(module=module)

                for name, obj in inspect.getmembers(object=module):
                    if (
                        inspect.isclass(object=obj)
                        and issubclass(obj, parent_class)
                        and (obj != parent_class)
                    ):
                        classes.append(obj)

        return classes

    def custom_parse_entry(
        self, wiktionary_entry: WiktionaryPageEntry
    ) -> CustomParsedWiktionaryPageEntry:
        """
        Parses an entry of a page.
        """

        # Instantiate all subclasses and run them
        results = {
            (instance := subclass(wiktionary_entry)).name: instance.run()
            for subclass in self.parser_classes
        }

        # Add the page name
        results["name"] = wiktionary_entry.page.name

        return CustomParsedWiktionaryPageEntry(**results)

    def _extract_word_types(
        self, content: dict[str, Any]
    ) -> list[CustomParsedWiktionaryPageEntry]:
        word_types = []

        page_id = content.get("pageid")
        name = content.get("title")
        wikitext = self._get_wikitext(content=content)

        if not page_id or not name or not wikitext:
            return word_types

        page = WiktionaryPage(
            page_id=page_id,
            name=name,
            wikitext=wikitext,
        )
        for entry in self.entries_from_page(page=page):
            results = self.custom_parse_entry(wiktionary_entry=entry)
            word_types.append(results)

        return word_types

    @staticmethod
    def _get_wikitext(content: dict[str, Any]) -> str | None:
        value = content.get("wikitext")
        if value:
            return value.get("*")
        return None

    @property
    def plural(self) -> str | None:
        return (
            "\n    ".join(
                f"{k}: {v}"
                for k, v in self.first_word.flexion.items()
                if "plural" in k.lower()
            )
            if self.first_word.flexion and self.first_word.flexion != ""
            else ""
        )

    @property
    def characteristics(self) -> str | None:
        return (
            "\n    ".join(f"{k}: {v}" for k, v in self.first_word.flexion.items())
            if self.first_word.flexion and self.first_word.flexion != ""
            else ""
        )

    @property
    def ipa(self) -> str | None:
        return ", ".join(self.first_word.ipa or [])

    @property
    def meaning(self) -> str | None:
        return "\n    ".join(
            c.strip().replace("\n", "")
            for c in (self.first_word.meaning or [])
            if c != "" and c.strip().replace("\n", "") != ""
        )

    @property
    def example1(self) -> str | None:
        return (
            self.first_word.example[0].strip().replace("\n", "")
            if self.first_word.example is not None and len(self.first_word.example)
            else ""
        )

    @property
    def example2(self) -> str | None:
        return (
            self.first_word.example[1].strip().replace("\n", "")
            if self.first_word.example is not None and len(self.first_word.example) > 1
            else ""
        )
