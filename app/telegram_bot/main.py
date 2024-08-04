import logging
from typing import Any, Callable, NamedTuple

from telegram import BotCommand, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram.ext._callbackcontext import CallbackContext
from telegram.ext._extbot import ExtBot
from telegram.ext._jobqueue import JobQueue

from app.private_config import bot_token
from app.telegram_bot.handlers import (
    handle_audio,
    handle_duden_word,
    handle_help,
    handle_verben_word,
    handle_web_word,
    handle_word,
    message_handle,
    unsupported_message_handle,
)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger: logging.Logger = logging.getLogger(name=__name__)


class CommandInfo(NamedTuple):
    command: str
    handler: Callable[..., Any]
    description: str


COMMANDS: list[CommandInfo] = [
    CommandInfo(
        command="w",
        handler=handle_word,
        description="Create an Anki note for a word",
    ),
    CommandInfo(
        command="a",
        handler=handle_audio,
        description="Create audio from text",
    ),
    CommandInfo(
        command="v",
        handler=handle_verben_word,
        description="Create an Anki note from verben",
    ),
    CommandInfo(
        command="d",
        handler=handle_duden_word,
        description="Create an Anki note from duden",
    ),
    CommandInfo(
        command="ww",
        handler=handle_web_word,
        description="Create an Anki note and send it to AnkiWeb",
    ),
    CommandInfo(
        command="help",
        handler=handle_help,
        description="Show help message",
    ),
]


async def post_init(application: Any) -> None:
    """
    Set bot commands after initializing the bot.

    Args:
        application (Application): The application object.
    """
    commands: list[BotCommand] = [
        BotCommand(command=f"/{command.command}", description=command.description)
        for command in COMMANDS
    ]
    await application.bot.set_my_commands(commands)


def main() -> None:
    """
    Run the bot.
    """
    application: Application[
        ExtBot[None],
        CallbackContext[ExtBot[None], dict[Any, Any], dict[Any, Any], dict[Any, Any]],
        dict[Any, Any],
        dict[Any, Any],
        dict[Any, Any],
        JobQueue[
            CallbackContext[
                ExtBot[None],
                dict[Any, Any],
                dict[Any, Any],
                dict[Any, Any],
            ]
        ],
    ] = Application.builder().token(token=bot_token).build()

    # Register words command handlers
    for command in COMMANDS:
        application.add_handler(
            handler=CommandHandler(
                command=command.command,
                callback=command.handler,
            )
        )
    # Register message handlers
    application.add_handler(
        handler=MessageHandler(
            filters=filters.TEXT & ~filters.COMMAND,
            callback=message_handle,
        )
    )
    application.add_handler(
        handler=MessageHandler(
            filters=filters.VIDEO & ~filters.COMMAND & filters.PHOTO,
            callback=unsupported_message_handle,
        )
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
