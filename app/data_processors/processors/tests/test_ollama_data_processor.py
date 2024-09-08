from typing import Any

import pytest

from app.data_processors.processors.ollama_data_processor import OllamaDataProcessor
from app.serializers import CustomFields, CustomNote


@pytest.fixture()  # type: ignore
def ollama_data_processor() -> OllamaDataProcessor:
    return OllamaDataProcessor()


@pytest.mark.vcr(mode="once")
def test_ollama_processor_get_anki_note_(
    ollama_data_processor: OllamaDataProcessor,
    initial_note: CustomNote,
    snapshot: Any,
) -> None:
    result: CustomNote | None = ollama_data_processor.get_note_data(
        word="Abend", note=initial_note
    )
    assert result, "Add note failed"
    assert result.fields, "The result does not match the snapshot"
    assert snapshot("json") == result.fields.model_dump(
        mode="python"
    ), "The result does not match the snapshot"


def test__generate_content_from_scratch_prompt(
    ollama_data_processor: OllamaDataProcessor,
    snapshot: Any,
) -> None:
    prompts: dict[str, Any] = (
        ollama_data_processor._generate_content_from_scratch_prompts(  # type: ignore
            word="Abend",
            json_schema=CustomFields.model_json_schema_to_generate_fields(),
        )
    )
    assert snapshot("json") == prompts, "The result does not match the snapshot"


@pytest.mark.vcr(mode="once")
def test_generate_sentence_examples(
    ollama_data_processor: OllamaDataProcessor,
    snapshot: Any,
) -> None:
    result: list[str] = ollama_data_processor.generate_sentence_examples(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result
