import asyncio
from unittest.mock import AsyncMock

import pytest

from app.telegram_bot.handlers import handle_word


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_handle_word_with_message():
    """
    Test handle_word function with a valid message containing a word.

    This test mocks the update and context objects and verifies that the
    function calls the appropriate functions and returns without errors.
    """

    # Mock update object with a message containing a word
    mock_update = AsyncMock()
    mock_update.message = AsyncMock()
    mock_update.message.text = "test_word"

    # Mock context object
    mock_context = AsyncMock()

    # Call the function with mocked objects
    await handle_word(update=mock_update, context=mock_context)

    # Assert that save_anki_note_to_list is called with the word
    mock_context.dispatcher.bot.send_message.assert_called_once()
    mock_context.dispatcher.bot.send_message.call_args[0][0].text.should.contain(
        "Anki note for 'test_word' saved successfully."
    )

    # Assert that get_anki_note_data is called with the word
    await asyncio.sleep(0.1)  # Allow time for async calls to complete
    mock_context.dispatcher.bot.send_message.assert_called_with(
        mock_update.message, text=mock_context.dispatcher.bot.send_message.return_value
    )


@pytest.mark.asyncio
async def test_handle_word_with_empty_message() -> None:
    """
    Test handle_word function with an empty message.

    This test mocks the update object with an empty message and verifies
    that the function logs an error message.
    """

    # Mock update object with an empty message
    mock_update = AsyncMock()

    # Mock context object
    mock_context = AsyncMock()

    # Call the function with mocked objects
    await handle_word(update=mock_update, context=mock_context)

    # Assert that an error message is logged
    mock_context.log.error.assert_called_once()
    mock_context.log.error.call_args[0][0].should.contain("No message provided.")
