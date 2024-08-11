from typing import Any, Callable
from unittest.mock import AsyncMock, patch

import pytest

from app.anki_connectors.anki_web_connector import AnkiWebConnector
from app.telegram_bot.handlers import (
    handle_audio,
    handle_duden_word,
    handle_help,
    handle_text_without_command,
    handle_verben_word,
    handle_web_word,
    handle_word,
    message_handle,
)


@pytest.mark.vcr()
@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("function_name", "handle_function"),
    [
        ("handle_word", handle_word),
        ("handle_audio", handle_audio),
        ("handle_help", handle_help),
        ("handle_web_word", handle_web_word),
        ("handle_verben_word", handle_verben_word),
        ("handle_duden_word", handle_duden_word),
        ("handle_text_without_command", handle_text_without_command),
        ("message_handle", message_handle),
    ],
)
async def test_handle_functions(
    function_name: str,
    handle_function: Callable[..., Any],
    caplog: Any,
    snapshot: Any,
) -> None:
    # Set up mock objects
    mock_update = AsyncMock()
    mock_update.message = AsyncMock()
    mock_update.message.text = "Abend"
    mock_context = AsyncMock()
    mock_context.args = ["Abend"]

    # Call the function with mocked objects
    await handle_function(update=mock_update, context=mock_context)

    assert snapshot(f"{function_name}.json") == sorted(
        r.message for r in caplog.records
    )
