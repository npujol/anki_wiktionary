import requests
import logging

from app.serializers import CustomNote, Note

logger = logging.getLogger(__name__)


class AnkiConnector:
    # Doc for anki-connect: https://foosoft.net/projects/anki-connect/index.html#card-actions
    available_actions = (
        "findCards",
        "cardsInfo",
        "createDeck",
        "deckNames",
        "deckNamesAndIds",
        "getDecks",
        "changeDeck",
        "getDeckConfig",
        "saveDeckConfig",
        "setDeckConfigId",
        "getDeckStats",
        "guiAddCards",
        "storeMediaFile",
        "retrieveMediaFile",
        "sync",
        "exportPackage",
        "importPackage",
        "addNote",
        "addNotes",
    )

    def __init__(self, server_url: str = "http://127.0.0.1:8765"):
        self.server_url = server_url

    def make_request(self, action, params={}):
        request_data = {"action": action, "params": params, "version": 6}
        response = requests.post(self.server_url, json=request_data).json()
        if len(response) != 2:
            raise Exception("response has an unexpected number of fields")
        if "error" not in response or "result" not in response:
            raise Exception("response is missing required error or result field")
        if response.get("error"):
            raise Exception(response.get("error"))
        return response.get("result")

    def get_available_decks(self):
        """
        Get the available decks using the make_request method and return the result.
        """
        return self.make_request("deckNamesAndIds")

    def get_cards_from_deck(self, deck_name: str):
        query = f"deck:{deck_name}"
        return self.make_request("findCards", {"query": query})

    def add_note(self, note: Note | CustomNote):
        data = note.model_dump(mode="python", by_alias=True, exclude_none=True)
        return self.make_request(
            "addNote",
            {"note": data},
        )

    def get_models_and_ids(self):
        return self.make_request("modelNamesAndIds")
