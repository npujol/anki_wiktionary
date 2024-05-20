import importlib.util
import inspect
from pathlib import Path

from wiktionary_de_parser import WiktionaryParser
from wiktionary_de_parser.models import WiktionaryPageEntry
from wiktionary_de_parser.parser import Parser

from app.parser.models import CustomParsedWiktionaryPageEntry


class CustomParser(WiktionaryParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        new_parsers = self.find_new_parser_classes()
        self.parser_classes = self.parser_classes + new_parsers

    @staticmethod
    def find_new_parser_classes():
        path = Path(__file__).parent / "new_parser"
        parent_class = Parser
        classes = []

        for child in path.iterdir():
            if (
                child.is_file()
                and child.name.endswith(".py")
                and child.name != "__init__.py"
            ):
                module_name = child.stem
                spec = importlib.util.spec_from_file_location(module_name, child)

                if not spec or not spec.loader:
                    raise Exception(f"Could not load {child}")

                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for name, obj in inspect.getmembers(module):
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, parent_class)
                        and (obj != parent_class)
                    ):
                        classes.append(obj)

        return classes

    def custom_parse_entry(self, wiktionary_entry: WiktionaryPageEntry):
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
