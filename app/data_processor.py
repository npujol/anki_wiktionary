import requests
from wiktionary_de_parser.models import ParsedWiktionaryPageEntry, WiktionaryPage
from app.parser.parser import CustomParser
from app.serializers import CustomFields, CustomNote


class WiktionaryDataProcessor:
    def __init__(self) -> None:
        self.base_url = "https://de.wiktionary.org/w/api.php"

    def get_wiktionary_data(self, word: str) -> list[ParsedWiktionaryPageEntry]:
        """
        Fetches data from Wiktionary for a given word and returns a list of
        ParsedWiktionaryPageEntry objects.

        Args:
            word (str): The word to fetch data for.

        Returns:
            list[ParsedWiktionaryPageEntry]: A list of ParsedWiktionaryPageEntry objects
            containing information about the word.
        """
        params = {
            "action": "parse",
            "page": word,
            "prop": "wikitext",
            "format": "json",
        }

        content = requests.get(self.base_url, params=params).json().get("parse")

        if not content:
            return []

        parser = CustomParser()
        page = WiktionaryPage(
            page_id=content.get("pageid"),
            name=content.get("title"),
            wikitext=content.get("wikitext").get("*"),
        )
        word_types: list[ParsedWiktionaryPageEntry] = []
        for entry in parser.entries_from_page(page):
            results = parser.custom_parse_entry(entry)
            word_types.append(results)
        return word_types


class NoteDataProcessor:
    def __init__(self, deck_name: str = "Test", model_name: str = "Basic_") -> None:
        self.data_handler = WiktionaryDataProcessor()
        self.deck_name = deck_name
        self.model_name = model_name

    # TODO: Update Note content
    def get_anki_note(self, word: str) -> CustomNote:
        content = self.data_handler.get_wiktionary_data(word)
        meaning = ""
        for item in content:
            for k, v in item.model_dump(
                mode="python",
                by_alias=True,
                exclude_none=True,
            ).items():
                meaning += f"{k}: {v}\n"

        note = CustomNote(
            deckName=self.deck_name,
            modelName=self.model_name,
            fields=CustomFields(
                full_word=word,
                plural="missing",
                # characteristics="missing",
                ipa=",".join(content[0].ipa),  # type: ignore
                # audio=content[0].audio,
                meaning=meaning,
                # meaning_spanish=content[0].meaning_spanish,
                # example1=content[0].example1,
                # example1e=content[0].example1e,
                # example2=content[0].example2,
                # example2e=content[0].example2e,
            ),
            tags=["test"],
            audio=[],
            video=[],
            picture=[],
        )

        return note
