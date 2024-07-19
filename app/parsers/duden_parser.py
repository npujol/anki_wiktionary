from typing import Any

from duden.word import DudenWord


class CustomDudenParser:
    def __init__(self, duden_word: DudenWord) -> None:
        self.duden_word = duden_word
        self.soup = duden_word.soup
        self.examples = self._extract_examples()

    def _extract_examples(self) -> list[Any]:
        # Find the <ul> element with the class 'note__list'
        note_list = self.soup.find("ul", class_="note__list")
        if note_list is None:
            return []
        # Extract all <li> elements within this <ul> element
        children = note_list.find_all("li")
        if children is None:
            return []
        examples = [li.get_text(strip=True) for li in children]
        return examples

    @property
    def example1(self):
        if self.examples:
            return self.examples[0]
        return ""

    @property
    def example2(self):
        if self.examples and len(self.examples) >= 2:
            return self.examples[1]
        return ""
