from typing import Any

from duden.word import DudenWord

from app.helpers import flatten_and_stringify


class CustomDudenParser:
    def __init__(self, duden_word: DudenWord) -> None:
        self.duden_word: DudenWord = duden_word
        self.soup = duden_word.soup
        self.examples: list[str] = self._extract_examples()

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
    def example1(self) -> str | None:
        if self.examples:
            return self.examples[0]
        return None

    @property
    def example2(self) -> str | None:
        if self.examples and len(self.examples) >= 2:
            return self.examples[1]
        return None

    @property
    def plural(self) -> str | None:
        if self.duden_word.grammar_overview:
            return flatten_and_stringify(content=self.duden_word.grammar_overview)
        return None

    @property
    def characteristics(self) -> str | None:
        result = None
        if self.duden_word.part_of_speech:
            result = flatten_and_stringify(content=self.duden_word.part_of_speech)

        if self.duden_word.usage:
            usage = flatten_and_stringify(content=self.duden_word.usage)
            if result is not None and usage is not None:
                result += "\n"
                result += usage
            else:
                result = usage
        return result

    @property
    def ipa(self) -> str | None:
        result = None
        if self.duden_word.word_separation:
            result = flatten_and_stringify(
                content=self.duden_word.word_separation, separator="|"
            )

        if self.duden_word.phonetic:
            phonetic = flatten_and_stringify(content=self.duden_word.phonetic)
            if result is not None and phonetic is not None:
                result += "\n"
                result += phonetic
            else:
                result = phonetic
        return result

    @property
    def meaning(self) -> str | None:
        result = None
        if self.duden_word.meaning_overview:
            result = flatten_and_stringify(
                content=self.duden_word.meaning_overview, separator="\n"
            )

        if self.duden_word.synonyms:
            synonyms = flatten_and_stringify(content=self.duden_word.synonyms)
            if result is not None and synonyms is not None:
                result += "\n"
                result += synonyms
            else:
                result = synonyms
        return result
