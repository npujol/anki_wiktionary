from wiktionary_de_parser import WiktionaryParser
import importlib.util
import inspect
from pathlib import Path

from wiktionary_de_parser.parser import Parser


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
