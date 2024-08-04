import asyncio
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from app.anki_connectors.anki_web_connector import AnkiWebConnector
from app.main import (
    add_audio_local,
    generate_audio,
    generate_note,
    generate_notes,
    get_anki_note_data,
    save_anki_note_to_list,
    send_card_using_anki_web,
)
from app.serializers import CustomNote


@pytest.mark.vcr()
def test_generate_notes_is_successful(snapshot: Any) -> None:
    result: bool = generate_note(word="Abend")
    assert result, "Add note failed"
    assert snapshot("json") == result, "The result does not match the snapshot"


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_get_anki_note_data_is_successful(
    snapshot: Any,
) -> None:
    result: CustomNote | None = await asyncio.create_task(
        coro=get_anki_note_data(word="Abend")
    )
    assert result, "Add note failed"
    assert snapshot("json") == result.model_dump(mode="python", by_alias=True)


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_generate_audio() -> None:
    """
    Tests the generate_audio function.
    """
    text: str = "Hello, world!"
    path: Path = await generate_audio(text=text)
    assert path.exists(), "The audio file was not generated."
    assert path.suffix == ".mp3", "The file is not an mp3."
    assert path.name == f"{text}.mp3", "The file name is incorrect."
    path.unlink()


@pytest.mark.vcr()
def test_add_audio_local(custom_note_obj: CustomNote) -> None:
    """
    Tests the generate_audio function.
    """
    note: CustomNote = add_audio_local(note=custom_note_obj)  # type: ignore
    assert note, "Add note failed"

    assert note.audio, "The audio field is not set."

    path: Path = Path(custom_note_obj.audio[0].url)
    assert path.exists(), "The audio file was not generated."
    assert path.suffix == ".mp3", "The file is not an mp3."
    path.unlink()


@pytest.mark.vcr()
def test_generate_notes(tmp_path: Path) -> None:
    temp_file: Path = Path(tmp_path) / "test.txt"
    temp_file.write_text(data="Abend")
    is_successful: bool = generate_notes(notes_path=temp_file)
    assert is_successful, "Add notes failed."
    temp_file.unlink()


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_save_anki_note_to_list(tmp_path: Path) -> None:
    file_path: Path = tmp_path / "test.txt"
    is_successful: bool = await save_anki_note_to_list(
        word="Abend", file_path=file_path
    )
    assert is_successful, "Add note failed."


@pytest.mark.vcr()
@pytest.mark.asyncio
@patch.object(target=AnkiWebConnector, attribute="close")
async def test_send_card_using_anki_web(close_mock: MagicMock) -> None:
    close_mock.return_value = None
    note: CustomNote | None = await send_card_using_anki_web(word="Abend")
    assert note, "Add note failed"

    assert note.audio, "The audio field is not set."
