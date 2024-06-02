from typing import Any

import pytest

from app.data_processor.note_data_processor import NoteDataProcessor
from app.data_processor.ollama_data_processor import OllamaDataProcessor
from app.data_processor.wiktionary_data_processor import WiktionaryDataProcessor
from app.serializers import CustomFields


@pytest.mark.vcr()
def test_get_wiktionary_data(snapshot: Any) -> None:
    result = WiktionaryDataProcessor().get_wiktionary_data(word="Abend")
    assert result, "Add note failed"
    for key, value in enumerate(iterable=result):
        assert snapshot(f"{value.name}_{key}.json") == value.model_dump(
            mode="python", by_alias=True, exclude_none=True
        ), "The result does not match the snapshot"


@pytest.mark.vcr()
def test_get_anki_note(snapshot: Any) -> None:
    result = NoteDataProcessor().get_anki_note(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result.model_dump(
        mode="python", by_alias=True, exclude_none=True
    ), "The result does not match the snapshot"


@pytest.mark.vcr(mode="always")
def test_ollama_processor_get_anki_note_(snapshot: Any) -> None:
    result = OllamaDataProcessor().get_anki_note(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result.model_dump(
        mode="python", by_alias=True, exclude_none=True
    ), "The result does not match the snapshot"


def test__generate_content_from_scratch_prompt(snapshot: Any) -> None:
    prompts = OllamaDataProcessor()._generate_content_from_scratch_prompts(
        word="Abend",
        json_schema=CustomFields.model_json_schema_to_generate_fields(),
    )
    assert snapshot("json") == prompts, "The result does not match the snapshot"
