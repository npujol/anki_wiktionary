import json
import logging
from typing import Any, Iterator, Mapping

from ollama import Client  # type: ignore

from app.data_processors.processors.base_data_processor import BaseDataProcessor
from app.private_config import ollama_server_url
from app.serializers import CustomFields

logger: logging.Logger = logging.getLogger(name=__name__)

# TODO: Set up a config file to configure the prompts


class OllamaDataProcessor(BaseDataProcessor):
    def __init__(self, deck_name: str = "Test", model_name: str = "Basic_") -> None:
        self.deck_name: str = deck_name
        self.model_name: str = model_name
        self.client = Client(host=ollama_server_url)
        self.fields_class = CustomFields

    def get_note_data(self, word: str) -> dict[str, Any]:
        prompts: dict[str, Any] = self._generate_content_from_scratch_prompts(
            word=word,
            json_schema=CustomFields.model_json_schema_to_generate_fields(),
        )
        fields: dict[str, Any] = {"full_word": word}
        for key, prompt in prompts.items():
            # TODO: Set up a config file to configure the model and prompt
            result: Mapping[str, Any] | Iterator[Mapping[str, Any]] = (
                self.client.generate(
                    model="llama3",
                    prompt=prompt,
                )
            )
            response: str | None = result.get("response")  # type: ignore

            if response is None:
                logger.error(
                    msg=f"Could not fetch data for field '{key}' using Ollama."
                )
                continue
            try:
                json_content: dict[str, Any] = json.loads(s=response)  # type: ignore
                content: str = "\n".join(str(v) for v in json_content.values())
            except json.JSONDecodeError as e:
                logger.exception(msg=f"Using raw string, due to {e}.")
                content: str = response  # type: ignore
            fields[key] = content

        return fields

    def generate_sentence_examples(
        self, word: str, count_examples: int = 1
    ) -> list[str]:
        prompt: str = (
            f"Gibt mir {count_examples}-Satz-Beispiele für das Wort: {word}."
            f"Das Ergebnis sollte eine JSON-Datei mit den Schluesseln: sentences"
            f"und eine Liste mit  {count_examples} Beispiele. "
            " Satzbeispielen sein ohne anderen Text oder Erklärung."
        )
        result: Mapping[str, Any] | Iterator[Mapping[str, Any]] = self.client.generate(
            model="llama3",
            prompt=prompt,
            format="json",
        )

        response: str | None = result.get("response")  # type: ignore
        return self._parse_response(response=response)  # type: ignore

    def _parse_response(self, response: str | None) -> list[str]:
        content: list[str] = []
        if response is None:
            return content
        try:
            json_content: dict[str, Any] = json.loads(s=response)  # type: ignore
            content = list(json_content.values())
        except json.JSONDecodeError as e:
            logger.exception(msg=f"Using raw string, due to {e}.")
            content = response  # type: ignore
        return content

    def _generate_content_from_scratch_prompts(
        self,
        word: str,
        json_schema: dict[str, Any],
    ) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in json_schema.items():
            prompt: str = (
                f"""**Generate Content from Word: {word}**"""
                f""" Given a word, generate a piece of content ({key}) based on"""
                f""" the following constraints: {value["description"]}"""
                f"""" **Word:*{word}* """
                """ **Constraints:**"""
                """ Use the constraints defined in the JSON schema."""
                """ **Generate Content:**"""
                f""" Using the word "{word}" as input, generate a JSON object with"""
                """ the key and the generated content."""
                """ Please return only the generated content without other text"""
                """ or explanation. The response should be in german."""
            )

            result[key] = prompt
        return result

    def _extract_from_content(self, word: str, content: Any) -> dict[str, Any]:
        raise NotImplementedError
