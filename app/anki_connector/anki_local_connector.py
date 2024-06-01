import logging
from typing import Any

import requests

from app.serializers import CustomNote, Note

logger = logging.getLogger(name=__name__)


class AnkiLocalConnector:
    # Doc for anki-connect: https://foosoft.net/projects/anki-connect/index.html#card-actions
    def __init__(self, server_url: str = "http://127.0.0.1:8765") -> None:
        self.server_url = server_url

    def make_request(self, action, params={}) -> dict[str, Any]:
        """
        Makes a request to the server with the specified action and parameters.

        Args:
            action (str): The action to be performed.
            params (dict): The parameters for the action. Defaults to an empty
            dictionary.

        Returns:
            The result of the request.
        """
        request_data = {"action": action, "params": params, "version": 6}
        response = requests.post(url=self.server_url, json=request_data).json()
        if len(response) != 2:
            msg = f"Response has an unexpected number of fields: {response}"
            logger.error(msg=msg)
            raise Exception(msg)
        if "error" not in response or "result" not in response:
            msg = f"Response is missing required error or result field: {response}"
            logger.error(msg=msg)
            raise Exception(msg)
        if response.get("error"):
            msg = f"Request failed: {response.get('error')}"
            logger.error(msg=msg)
            raise Exception(msg)
        return response.get("result")

    def get_available_decks(self) -> dict[str, Any]:
        """
        Retrieve available decks and their IDs.

        Args:
            self: The instance of the class.

        Returns:
            dict[str, Any]: A dictionary containing the available deck names and
            their corresponding IDs.
        """
        return self.make_request(action="deckNamesAndIds")

    def get_cards_from_deck(self, deck_name: str) -> dict[str, Any]:
        """
        Get cards from the specified deck.

        Args:
            deck_name (str): The name of the deck to retrieve cards from.

        Returns:
            dict: The response from the 'findCards' request.
        """
        query = f"deck:{deck_name}"
        return self.make_request(
            action="findCards",
            params={"query": query},
        )

    def add_note(self, note: Note | CustomNote) -> dict[str, Any]:
        """
        Adds a note to the system.

        Args:
            note: The note to be added. It can be either a Note or a CustomNote object.

        Returns:
            The result of the make_request method with the "addNote" endpoint
            and the note data.
        """
        data = note.model_dump(
            mode="python",
            by_alias=True,
            exclude_none=True,
        )
        return self.make_request(
            action="addNote",
            params={"note": data},
        )

    def get_models_and_ids(self) -> dict[str, Any]:
        """
        Get the model names and ids using the make_request method and return the
        result.

        Returns:
            The result of the make_request method with the "modelNamesAndIds" endpoint
            and the note data.
        """
        return self.make_request(action="modelNamesAndIds")
