import logging
from typing import Any

import requests

from app.serializers import CustomNote, Note, ToUpdateNote

from .errors import CollectionNotFoundError, ResultNotFoundError

logger: logging.Logger = logging.getLogger(name=__name__)


class AnkiLocalConnector:
    # Doc for anki-connect: https://foosoft.net/projects/anki-connect/index.html#card-actions
    def __init__(self, server_url: str = "http://127.0.0.1:8765") -> None:
        self.server_url: str = server_url

    def health_check(self) -> bool:
        try:
            self.make_request(action="deckNamesAndIds")
            return True
        except Exception:
            return False

    def make_request(
        self,
        action: str,
        params: dict[str, Any] = {},
    ) -> dict[str, Any]:
        """
        Makes a request to the server with the specified action and parameters.

        Args:
            action (str): The action to be performed.
            params (dict): The parameters for the action. Defaults to an empty
            dictionary.

        Returns:
            The result of the request.
        """
        request_data: dict[str, Any] = {
            "action": action,
            "params": params,
            "version": 6,
        }
        response: dict[str, dict[str, Any]] = requests.post(
            url=self.server_url, json=request_data
        ).json()

        if response.get("error") is not None:
            msg = f"Request failed: {response.get('error')}"
            logger.error(msg=msg)
            raise CollectionNotFoundError(msg)

        response_result: dict[str, Any] | None = response.get("result")
        if response_result is None:
            msg: str = (
                f"Response does not contain a result field. Response: {response}."
            )
            logger.error(msg=msg)
            raise ResultNotFoundError(msg)

        return response_result

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
        card_ids = list(
            self.make_request(
                action="findCards",
                params={"query": query},
            )
        )
        return self.make_request(
            action="cardsInfo",
            params={"cards": card_ids},
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
        data: dict[str, Any] = note.model_dump(
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

    async def add_audio_to_card(self, note: CustomNote) -> dict[str, Any]:
        await note.add_audio()
        note_json = note.model_dump(
            mode="python",
        )
        return self.make_request(
            action="updateNoteFields",
            params={"note": note_json},
        )

    async def add_missing_audios(self):
        decks = self.get_available_decks()
        updated_cards = []
        total_cards = 0
        for deck in decks:
            logger.info(f"Processing Deck: {deck}")
            for card in self.get_cards_from_deck(deck_name=deck):
                total_cards += 1
                # logger.info(f"Processing Card: {card}")
                try:
                    note: ToUpdateNote = ToUpdateNote.model_validate(card, strict=False)
                    if note.fields.audio is not None and note.fields.audio != "":
                        continue
                    await self.add_audio_to_card(note)
                    updated_cards.append(note.id)
                except Exception as e:
                    logger.info(e)
                    continue

        logger.info(f"{len(updated_cards)}/{total_cards}")

        if len(updated_cards) == 0:
            return
        self.make_request(action="forgetCards", params={"cards": [updated_cards]})
