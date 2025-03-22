from playwright.sync_api import Page


class CustomDWDSParser:
    """Parses DWDS website structure to extract linguistic data."""

    def __init__(self, page: Page):
        self.page = page

    @property
    def full_word(self) -> str:
        return self.page.query_selector("h1.dwdswb-ft-lemma").inner_text()

    @property
    def plural(self) -> str:
        if plural := self.page.query_selector(".dwdswb-ft-flexion .plural"):
            return plural.inner_text()
        return ""

    @property
    def part_of_speech(self) -> str:
        return self.page.query_selector(".dwdswb-ft-wortart").inner_text()

    @property
    def ipa(self) -> str:
        return self.page.query_selector(".dwdswb-ft-ipa").inner_text()

    @property
    def meaning(self) -> str:
        return "\n".join(
            [
                el.inner_text()
                for el in self.page.query_selector_all(".dwdswb-ft-bedeutungen li")
            ]
        )

    @property
    def examples(self) -> list[str]:
        return [
            el.inner_text()
            for el in self.page.query_selector_all(".dwdswb-ft-beispiele li")
        ]

    @property
    def usage_frequency(self) -> str:
        return self.page.query_selector(".dwdswb-ft-worthaeufigkeit").inner_text()
