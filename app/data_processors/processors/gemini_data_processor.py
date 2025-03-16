import json
from typing import Any

import google.generativeai as genai
from google.generativeai.types.generation_types import GenerateContentResponse

from app.private_config import gemini_api_key
from app.serializers import CustomFields, CustomNote

from .base_data_processor import BaseDataProcessor


class GeminiDataProcessor(BaseDataProcessor):
    def __init__(self) -> None:
        self.fields_class = CustomFields

        genai.configure(api_key=gemini_api_key)  # type: ignore
        self.client = genai.GenerativeModel(model_name="gemini-1.5-flash")  # type: ignore

        super().__init__()

    def get_note_data_per_field(self, word: str, note: CustomNote) -> CustomNote | None:
        content_dict: dict[str, str] = {"full_word": word}
        current_note_dict: dict[str, Any] = note.model_dump()

        for key, field in CustomFields.model_json_schema_to_generate_fields().items():
            if (
                key not in note.model_fields
                and current_note_dict.get(key, None) is not None
                and "ignored" not in field.get("description", "")
            ):
                self.logger.debug(msg=f"Skipping field '{key}'")
                continue
            try:
                prompt: str = f"Word: '{word}'. {field.get('description', '')} The answer should be in german."
                response: GenerateContentResponse = self.client.generate_content(
                    contents=prompt
                )

                if not response:
                    self.logger.warning(
                        msg=f"Could not fetch data for word '{word}' using Gemini."
                    )
                    continue
            except Exception as e:
                self.logger.warning(
                    msg=f"Could not fetch data for word '{word}' using Gemini due to {e}."
                )
                continue
            content_dict[key] = response.text

        updated_note: CustomNote | None = note.import_from_content(
            content=content_dict, fields_class=self.fields_class
        )
        return updated_note

    def get_note_data(self, word: str, note: CustomNote) -> CustomNote | None:
        content_dict: dict[str, str] = {"full_word": word}
        current_note_dict: dict[str, Any] = note.model_dump()
        requirements = []

        # Collect all field requirements first
        for key, field in CustomFields.model_json_schema_to_generate_fields().items():
            if (
                key not in note.model_fields
                and current_note_dict.get(key, None) is not None
                and "ignored" not in field.get("description", "")
            ):
                self.logger.debug(f"Skipping field '{key}'")
                continue
            requirements.append(f"{key}: {field.get('description', '')}")

        if not requirements:
            return note.import_from_content(content_dict, self.fields_class)

        # Single AI call with all requirements
        try:
            prompt = (
                f"Word: '{word}'. Provide all following information in German as JSON:\n"
                + "\n".join(requirements)
                + "\nFormat response as {{'field1': 'value1', 'field2': 'value2'}}"
            )

            response = self.client.generate_content(prompt)

            if not response:
                self.logger.warning(f"Failed to generate content for '{word}'")
                return None

            # Parse the single response
            ai_data = json.loads(response.text.strip("```json\n").rstrip("\n```"))
            content_dict.update(ai_data)

        except Exception as e:
            self.logger.warning(f"AI processing failed for '{word}': {str(e)}")
            return None

        return note.import_from_content(content_dict, self.fields_class)

    def _extract_from_content(self, word: str, content: Any) -> dict[str, Any]:
        raise NotImplementedError
