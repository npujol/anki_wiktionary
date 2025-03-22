from typing import Any

from playwright.sync_api import Page, sync_playwright

from app.parsers import CustomDWDSParser
from app.serializers import CustomFields, CustomNote

from .base_data_processor import BaseDataProcessor


class DWDSDataProcessor(BaseDataProcessor):
    def __init__(self) -> None:
        self.base_url = "https://www.dwds.de/wb/"
        self.fields_class = CustomFields
        super().__init__()

    def get_note_data(self, word: str, note: CustomNote) -> CustomNote | None:
        """
        Fetches data from DWDS for a given word and updates the note.

        Args:
            word (str): The target word to look up.
            note (CustomNote): Note object to populate with data.

        Returns:
            CustomNote | None: Updated note or original note if data not found.
        """
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context()
            page = context.new_page()

            try:
                page.goto(f"{self.base_url}{word}")
                breakpoint()
                # Check if word page exists
                if page.query_selector(".dwdswb-ft-error"):
                    self.logger.error(f"Word '{word}' not found on DWDS")
                    return note

                # Wait for critical content to load
                page.wait_for_selector(".dwdswb-ft-blocks-wrapper", timeout=5000)

                # Extract data from page
                content_dict = self._extract_from_content(page)
                updated_note = note.import_from_content(
                    content=content_dict, fields_class=self.fields_class
                )
                return updated_note

            except Exception as e:
                self.logger.error(f"Error processing '{word}': {str(e)}")
                return note
            finally:
                context.close()
                browser.close()

    def _extract_from_content(self, page: Page) -> dict[str, Any]:
        """Extracts structured data from DWDS page using custom parser."""
        parser = CustomDWDSParser(page=page)
        return {
            "full_word": parser.full_word,
            "plural": parser.plural,
            "part_of_speech": parser.part_of_speech,
            "ipa": parser.ipa,
            "meaning": parser.meaning,
            "examples": parser.examples,
            "usage_frequency": parser.usage_frequency,
        }
