import asyncio
from pathlib import Path
from typing import Any

import pytest

from app.handlers import AnkiHandler
from app.serializers import CustomNote


@pytest.mark.asyncio
@pytest.mark.vcr()
async def test_generate_notes_is_successful(
    anki_handler: AnkiHandler, snapshot: Any
) -> None:
    result: bool = await anki_handler.generate_note(
        word="Morgen", processor_name="wiktionary"
    )

    assert result, "Add note failed"
    assert snapshot("json") == result, "The result does not match the snapshot"


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_get_anki_note_data_is_successful(
    anki_handler: AnkiHandler,
    snapshot: Any,
) -> None:
    result: Any = await asyncio.create_task(
        coro=anki_handler.get_anki_note_data(word="Abend", processor_name="wiktionary")  # type: ignore
    )
    assert result, "Add note failed"
    assert snapshot("json") == result.model_dump(mode="python", by_alias=True)


@pytest.mark.asyncio()
@pytest.mark.vcr()
async def test_generate_notes(anki_handler: AnkiHandler, tmp_path: Path) -> None:
    temp_file: Path = Path(tmp_path) / "test.txt"
    temp_file.write_text(data="Abend")
    is_successful: bool = await anki_handler.generate_notes(notes_path=temp_file)
    assert is_successful, "Add notes failed."
    temp_file.unlink()


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_save_anki_note_to_list(
    anki_handler: AnkiHandler, tmp_path: Path
) -> None:
    file_path: Path = tmp_path / "test.txt"
    is_successful: bool = await anki_handler.save_anki_note_to_list(
        word="Abend", file_path=file_path
    )
    assert is_successful, "Add note failed."


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_send_card_using_anki_web(anki_handler: AnkiHandler) -> None:
    note: CustomNote | None = await anki_handler.send_card_using_anki_web(
        word="Abend", processor_name="wiktionary"
    )
    assert note, "Add note failed"

    assert note.audio, "The audio field is not set."
