from typing import Any, Callable
from unittest.mock import AsyncMock

import pytest

from app.telegram_bot import BotHandler


@pytest.mark.vcr()
@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("function_name", "handle_function"),
    [
        ("handle_word", BotHandler().handle_word),
        ("handle_audio", BotHandler().handle_audio),
        ("handle_help", BotHandler().handle_help),
        ("handle_web_word", BotHandler().handle_web_word),
        ("handle_verben_word", BotHandler().handle_verben_word),
        ("handle_duden_word", BotHandler().handle_duden_word),
        ("handle_text_without_command", BotHandler().handle_text_without_command),
        ("message_handle", BotHandler().message_handle),
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
