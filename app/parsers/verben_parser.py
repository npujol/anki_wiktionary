from typing import Any

from bs4 import BeautifulSoup, NavigableString, Tag

from app.helpers import flatten_and_stringify
from app.html_processors import clean_text


class VerbenParser:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup: BeautifulSoup = soup
        self.examples: list[str] = self._extract_examples()

    def _extract_examples(self) -> list[Any]:
        example_list: list[str] = []
        examples_div: Tag | NavigableString | None = self.soup.find(
            "div", class_="rAufZu"
        )
        if examples_div is None:
            return example_list

        examples = examples_div.find_all("p")  # type: ignore
        for sentence in examples:  # type: ignore
            if hasattr(sentence, "text"):  # type: ignore
                example_list.append(clean_text(sentence.text))  # type: ignore
        return example_list

    @property
    def info_element(self) -> Tag | None:
        info_selector = "body > article > div:nth-child(1) > div.rAbschnitt"

        # Find the elements using the CSS selectors
        info_element: Tag | None = self.soup.select_one(selector=info_selector)
        return info_element

    @property
    def lateral_info_element(self) -> Tag | None:
        lateral_info_selector = "body > article > div:nth-child(1) > div.rInfo"

        lateral_info_element: Tag | None = self.soup.select_one(
            selector=lateral_info_selector
        )
        return lateral_info_element

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
        result: str | None = None
        # Find the elements using the CSS selectors
        if self.info_element is None:
            return result

        plural_element = self.info_element.find("span", class_="rInf")

        if plural_element is not None:
            # remove soft hyphens "\xad" and return
            return ", ".join(
                [
                    span["title"]
                    for span in plural_element.find_all("span")  # type: ignore
                    if "title" in span.attrs  # type: ignore
                ]  # type: ignore
            )  # type: ignore

        return result

    @property
    def characteristics(self) -> str | None:
        result: str | None = None
        if self.info_element is None:
            return result

        plural_element = self.info_element.find("span", class_="rInf")  # type: ignore

        if plural_element is not None:
            # remove soft hyphens "\xad" and return
            return ", ".join(
                [
                    span["title"]
                    for span in plural_element.find_all("span")  # type: ignore
                    if "title" in span.attrs  # type: ignore
                ]  # type: ignore
            )  # type: ignore

        return result

    @property
    def ipa(self) -> str | None:
        result: str | None = None
        # Note: The ipa is not in this website
        return result

    @property
    def meaning(self) -> str | None:
        result: str | None = None
        if self.info_element is None:
            return result

        meaning_element: Tag | NavigableString | None = self.info_element.find_all(
            "span", class_="rInf"
        )  # type: ignore

        if meaning_element is None:
            return result

        result = ""
        for span in meaning_element:  # type: ignore
            if "title" in span.attrs:  # type: ignore
                result += "\n" + span["title"]  # type: ignore
            if hasattr(span, "text"):  # type: ignore
                result += "\n" + flatten_and_stringify(content=span.text)  # type: ignore

        return result  # type: ignore
