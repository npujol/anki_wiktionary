from typing import Any

import pytest

from app.data_processors.processors.ollama_data_processor import OllamaDataProcessor
from app.serializers import CustomFields


@pytest.fixture()
def ollama_data_processor() -> OllamaDataProcessor:
    return OllamaDataProcessor()


@pytest.mark.vcr(mode="once")
def test_ollama_processor_get_anki_note_(
    ollama_data_processor: OllamaDataProcessor,
    snapshot: Any,
) -> None:
    result = ollama_data_processor.get_note_data(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result, "The result does not match the snapshot"


def test__generate_content_from_scratch_prompt(
    ollama_data_processor: OllamaDataProcessor,
    snapshot: Any,
) -> None:
    prompts = ollama_data_processor._generate_content_from_scratch_prompts(
        word="Abend",
        json_schema=CustomFields.model_json_schema_to_generate_fields(),
    )
    assert snapshot("json") == prompts, "The result does not match the snapshot"


@pytest.mark.vcr(mode="once")
def test_generate_sentence_examples(
    ollama_data_processor: OllamaDataProcessor,
    snapshot: Any,
) -> None:
    result = ollama_data_processor.generate_sentence_examples(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result
