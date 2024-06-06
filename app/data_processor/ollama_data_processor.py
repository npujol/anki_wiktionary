import json
import logging
from typing import Any

from ollama import Client

from app.private_config import ollama_server_url
from app.serializers import CustomFields, CustomNote

logger = logging.getLogger(name=__name__)

# TODO: Set up a config file to configure the prompts


class OllamaDataProcessor:
    def __init__(self, deck_name: str = "Test", model_name: str = "Basic_") -> None:
        self.deck_name = deck_name
        self.model_name = model_name
        self.client = Client(host=ollama_server_url)

    def get_anki_note(self, word: str) -> CustomNote:
        prompts = self._generate_content_from_scratch_prompts(
            word=word,
            json_schema=CustomFields.model_json_schema_to_generate_fields(),
        )
        fields: dict[str, Any] = {"full_word": word}
        for key, prompt in prompts.items():
            # TODO: Set up a config file to configure the model and prompt
            result = self.client.generate(
                model="llama3",
                prompt=prompt,
            )

            response = result.get("response", "")  # type: ignore
            try:
                json_content = json.loads(response)
                content = "\n".join(str(v) for v in json_content.values())
            except json.JSONDecodeError:
                isinstance(response, str)
                content = response
            fields[key] = content

        note = CustomNote(
            deckName=self.deck_name,
            modelName=self.model_name,
            fields=CustomFields(**fields),
            tags=["test"],
            audio=[],
            video=[],
            picture=[],
        )

        return note

    def _generate_content_from_scratch_prompts(
        self,
        word: str,
        json_schema: dict[str, Any],
    ) -> dict[str, Any]:
        result = {}
        for key, value in json_schema.items():
            prompt = f"""**Generate Content from Word: {word}**
                    Given a word, generate a piece of content ({key}) based on the following constraints: {value["description"]}

                    **Word:*{word}* ""

                    **Constraints:**
                    Use the constraints defined in the JSON schema.

                    **Generate Content:**
                    Using the word "{word}" as input, generate a JSON object with the key and the generated content. 
                    Please return only the generated content without other text or explanation. The response should be in german."""

            result[key] = prompt
        return result

    def generate_sentence_examples(
        self, word: str, count_examples: int = 1
    ) -> list[str]:
        prompt = (
            f"Gibt mir {count_examples}-Satz-Beispiele für das Wort: {word}."
            f"Das Ergebnis sollte eine JSON-Datei mit den Schluesseln: sentences und eine Liste mit  {count_examples} Beispiele. "
            " Satzbeispielen sein ohne anderen Text oder Erklarung."
        )
        result = self.client.generate(
            model="llama3",
            prompt=prompt,
            format="json",
        )

        response = result.get("response")  # type: ignore
        content = []
        if response is None:
            return content
        try:
            json_content = json.loads(response)
            content = list(json_content.values())
        except json.JSONDecodeError as e:
            logger.exception(f"Using raw string, due to {e}.")
            isinstance(response, str)
            content = response
        return content
