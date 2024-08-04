from typing import Any

from bs4 import BeautifulSoup, NavigableString, ResultSet, Tag
from duden.word import DudenWord  # type: ignore

from app.helpers import flatten_and_stringify


class CustomDudenParser:
    def __init__(self, duden_word: DudenWord) -> None:
        self.duden_word: DudenWord = duden_word
        self.soup: BeautifulSoup = duden_word.soup
        self.examples: list[str] = self._extract_examples()

    def _extract_examples(self) -> list[Any]:
        # Find the <ul> element with the class 'note__list'
        note_list: Tag | NavigableString | None = self.soup.find(
            name="ul", class_="note__list"
        )
        if note_list is None:
            return []
        # Extract all <li> elements within this <ul> element
        children: ResultSet[Any] = note_list.find_all("li")  # type: ignore
        if children is None:
            return []
        examples: list[Any] = [li.get_text(strip=True) for li in children]  # type: ignore
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
        if (
            hasattr(self.duden_word, "grammar_overview")
            and self.duden_word.grammar_overview  # type: ignore
        ):
            return flatten_and_stringify(content=self.duden_word.grammar_overview)  # type: ignore
        return None

    @property
    def characteristics(self) -> str | None:
        result: str | None = None
        if (
            hasattr(self.duden_word, "part_of_speech")
            and self.duden_word.part_of_speech  # type: ignore
        ):
            result = flatten_and_stringify(content=self.duden_word.part_of_speech)  # type: ignore

        if hasattr(self.duden_word, "usage") and self.duden_word.usage:  # type: ignore
            usage: str | None = flatten_and_stringify(content=self.duden_word.usage)  # type: ignore
            if result is not None and usage:
                result += "\n"
                result += usage
            else:
                result = usage
        return result

    @property
    def ipa(self) -> str | None:
        result: str | None = None
        if (
            hasattr(self.duden_word, "word_separation")
            and self.duden_word.word_separation  # type: ignore
        ):
            result = flatten_and_stringify(
                content=self.duden_word.word_separation,  # type: ignore
                separator="|",
            )

        if hasattr(self.duden_word, "phonetic") and self.duden_word.phonetic:  # type: ignore
            phonetic: str = flatten_and_stringify(content=self.duden_word.phonetic)  # type: ignore
            if result is not None and phonetic:
                result += "\n"
                result += phonetic
            else:
                result = phonetic
        return result

    @property
    def meaning(self) -> str | None:
        result: str | None = None
        if (
            hasattr(self.duden_word, "meaning_overview")
            and self.duden_word.meaning_overview  # type: ignore
        ):
            result = flatten_and_stringify(
                content=self.duden_word.meaning_overview,  # type: ignore
                separator="\n",
            )

        if hasattr(self.duden_word, "synonyms") and self.duden_word.synonyms:  # type: ignore
            synonyms: str = flatten_and_stringify(content=self.duden_word.synonyms)  # type: ignore
            if result is not None and synonyms:
                result += "\n"
                result += synonyms
            else:
                result = synonyms
        return result
