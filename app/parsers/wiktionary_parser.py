import importlib.util
import inspect
from importlib.machinery import ModuleSpec
from pathlib import Path
from typing import Any

from wiktionary_de_parser import WiktionaryParser  # type: ignore
from wiktionary_de_parser.models import (  # type: ignore
    WiktionaryPage,
    WiktionaryPageEntry,
)
from wiktionary_de_parser.parser import Parser  # type: ignore

from .models import CustomParsedWiktionaryPageEntry


class CustomWiktionaryParser(WiktionaryParser):
    def __init__(self, content: dict[str, str], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        new_parsers: list[Any] = self.find_new_parser_classes()
        self.parser_classes = self.parser_classes + new_parsers
        self.word_types: list[CustomParsedWiktionaryPageEntry] = (
            self._extract_word_types(content=content)
        )
        self.first_word: CustomParsedWiktionaryPageEntry = self.word_types[0] or None

    @staticmethod
    def find_new_parser_classes() -> list[Any]:
        path: Path = Path(__file__).parent / "wiktionary"
        parent_class = Parser
        classes: list[Any] = []

        for child in path.iterdir():
            if (
                child.is_file()
                and child.name.endswith(".py")
                and child.name != "__init__.py"
            ):
                module_name: str = child.stem
                spec: ModuleSpec | None = importlib.util.spec_from_file_location(
                    name=module_name, location=child
                )

                if not spec or not spec.loader:
                    raise Exception(f"Could not load {child}")

                module: Any = importlib.util.module_from_spec(spec=spec)
                spec.loader.exec_module(module=module)

                for _, obj in inspect.getmembers(object=module):
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
        results: dict[str, Any] = {
            (instance := subclass(wiktionary_entry)).name: instance.run()  # type: ignore
            for subclass in self.parser_classes
        }

        # Add the page name
        results["name"] = wiktionary_entry.page.name

        return CustomParsedWiktionaryPageEntry(**results)

    def _extract_word_types(
        self, content: dict[str, Any]
    ) -> list[CustomParsedWiktionaryPageEntry]:
        word_types: list[CustomParsedWiktionaryPageEntry] = []

        page_id: int | None = content.get("pageid")
        name: str | None = content.get("title")
        wikitext: str | None = self._get_wikitext(content=content)

        if not page_id or not name or not wikitext:
            return word_types

        page = WiktionaryPage(
            page_id=page_id,
            name=name,
            wikitext=wikitext,
        )
        for entry in self.entries_from_page(page=page):  # type: ignore
            results: CustomParsedWiktionaryPageEntry = self.custom_parse_entry(
                wiktionary_entry=entry  # type: ignore
            )
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
                for k, v in self.first_word.flexion.items()  # type: ignore
                if "plural" in k.lower()  # type: ignore
            )
            if self.first_word.flexion and self.first_word.flexion != ""  # type: ignore
            else ""
        )

    @property
    def characteristics(self) -> str | None:
        return (
            "\n    ".join(f"{k}: {v}" for k, v in self.first_word.flexion.items())  # type: ignore
            if self.first_word.flexion and self.first_word.flexion != ""  # type: ignore
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
