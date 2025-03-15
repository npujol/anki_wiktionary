import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from app.anki_connectors import AnkiLocalConnector, AnkiWebPyConnector
from app.data_processors import NoteDataProcessor
from app.private_config import (
    anki_deck_name,
    anki_note_file_path,
    anki_password,
    anki_username,
)
from app.serializers import CustomNote

# from .errors import NoAnkiConnectorError


class AnkiHandler:
    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(name=__name__)
        self.connectors: dict[str, Any] = self._setup_connectors()

    def _setup_connectors(self) -> dict[str, Any]:
        connectors: dict[str, Any] = {}
        if not anki_username or not anki_password:
            self.logger.warning(
                msg="Anki credentials not provided. Skipping Anki connector."
            )

            web_connector = AnkiWebPyConnector(
                username=anki_username,
                password=anki_password,
            )
            connectors["web"] = web_connector

        local_connector = AnkiLocalConnector()

        if not local_connector.health_check():
            self.logger.warning(
                msg="Anki local connector not available. Skipping Anki connector."
            )

            connectors["local"] = local_connector

        # if not connectors:
        #     raise NoAnkiConnectorError("No Anki connector available.")

        return connectors

    def is_local_connector_available(self) -> bool:
        return "local" in self.connectors

    def is_web_connector_available(self) -> bool:
        return "web" in self.connectors

    def get_connector(self, name: str) -> Any:
        if name not in self.connectors:
            raise ValueError(f"Anki connector {name} not available.")

        return self.connectors[name]

    async def generate_note(self, word: str, processor_name: str | None = None) -> bool:
        """
        Generate Anki note for a given word and add it to Anki database.

        Args:
            word (str): The word for which the Anki note is to be created.

        Returns:
            bool: True if the Anki note is created successfully, False otherwise.
        """
        try:
            self.logger.info(msg=f"Creating Anki note for {word}")

            note: CustomNote | None = NoteDataProcessor(
                deck_name=anki_deck_name, model_name="Basic_"
            ).get_anki_note(word=word, processor_name=processor_name)
            if not note:
                self.logger.error(msg=f"Anki note for {word=} could not be created.")
                return False

            await note.add_audio()
            id: dict[str, Any] = AnkiLocalConnector().add_note(note=note)
            self.logger.info(msg=f"Note of {word=} with {id=} was created.")
        except Exception as e:
            self.logger.exception(
                msg=f"Anki note for {word=} could not be created, due to {e}."
            )
            return False
        return True

    async def get_anki_note_data(
        self, word: str, processor_name: str | None
    ) -> CustomNote | None:
        """
        Asynchronously retrieves Anki note data for a given word.

        Args:
            word (str): The word for which to retrieve Anki note data.

        Returns:
            NoteData: The Anki note data for the specified word.
        """
        note: CustomNote | None = NoteDataProcessor().get_anki_note(
            word=word, processor_name=processor_name
        )
        if note is not None:
            return await note.add_audio()

    async def save_anki_note_to_list(
        self, word: str, file_path: Path | str = anki_note_file_path
    ) -> bool:
        """
        Asynchronous function to save an Anki note to a list.

        Args:
            word (str): The word to be saved as a note.

        Returns:
            bool: True if the Anki note is saved successfully, False otherwise.
        """

        is_successful = False

        try:
            with open(file=file_path, mode="a") as file:
                file.write(f"{word}\n")
                self.logger.info(
                    msg=f"Anki note created: {datetime.now().isoformat()}: {word}"
                )
            is_successful = True
        except Exception as e:
            self.logger.exception(msg=f"Anki note could not be created, due to {e}.")
        return is_successful

    async def generate_notes(
        self, notes_path: Path | str = anki_note_file_path
    ) -> bool:
        """
        A function to generate notes from a file and write them back to the file.
        """

        try:
            with open(file=notes_path, mode="r") as file:
                words: list[str] = file.readlines()
            for word in set(words):
                self.logger.info(msg=f"Generating Anki note for {word}")
                try:
                    word: str = word.strip()
                    await self.generate_note(word=word)
                except Exception as e:
                    self.logger.exception(msg=f"Anki notes, due to {e}.")
                    continue
            with open(file=notes_path, mode="w") as file:
                words = file.truncate()  # type: ignore
        except Exception as e:
            self.logger.error(msg=f"Anki notes, due to {e}.")
            return False
        return True

    async def send_card_using_anki_web(
        self,
        word: str,
        processor_name: Optional[str] = None,
        deck_name: str = anki_deck_name,
        model_name: str = "Basic_",
    ) -> Optional[CustomNote]:
        """
        Asynchronously sends an Anki note to AnkiWeb.

        Args:
            word (str): The word to be sent to AnkiWeb.
            deck_name (str, optional): The name of the deck. Defaults to "Mein Deutsch".
            model_name (str, optional): The name of the model. Defaults to "Basic_".
            processor_name (str, optional): The name of the processor.
            Defaults to "wiktionary".
        Returns:
            CustomNote: The Anki note that was sent to AnkiWeb.
        """
        username: str = anki_username
        password: str = anki_password

        if not username or not password:
            self.logger.error(msg="Username or password not set.")
            return

        # Create Anki note
        self.logger.info(msg=f"Creating Anki note for {word}")
        note: CustomNote | None = NoteDataProcessor(
            deck_name=deck_name,
            model_name=model_name,
        ).get_anki_note(
            word=word,
            processor_name=processor_name,
        )

        if not note:
            self.logger.error(msg=f"Anki note for {word=} could not be created.")
            return

        await note.add_audio()

        # Send note to Anki web interface
        web_anki_connector = AnkiWebPyConnector(
            username=username,
            password=password,
        )
        self.logger.info(
            msg=(
                f"Sending Anki note for {word} to AnkiWeb using {deck_name=} "
                f"and {model_name}."
            )
        )
        await web_anki_connector.start()
        is_successful: bool = await web_anki_connector.send_card(
            custom_note=note,
            tags=[
                deck_name,
                model_name,
                datetime.now().isoformat(),
            ],
            card_type=note.card_type,  # type: ignore
        )
        await web_anki_connector.close()

        if not is_successful:
            self.logger.error(msg=f"Anki note for {word=} could not be created.")
            return

        self.logger.info(msg=f"Note of {word=} was created successfully.")
        return note
