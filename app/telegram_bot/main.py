import logging

from telegram import BotCommand, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from app.private_config import bot_token
from app.telegram_bot.handlers import (
    handle_audio,
    handle_help,
    handle_web_word,
    handle_word,
    message_handle,
    unsupported_message_handle,
)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(name=__name__)


async def post_init(application: Application) -> None:
    """
    Set bot commands after initializing the bot.

    Args:
        application (Application): The application object.
    """
    await application.bot.set_my_commands(
        [
            BotCommand(command="/word", description="Create an Anki note for a word"),
            BotCommand(command="/help", description="Show help message"),
            BotCommand(command="/audio", description="Create audio from text"),
            BotCommand(
                command="/web_word",
                description="Create an Anki note and send it to AnkiWeb",
            ),
        ]
    )


def main() -> None:
    """
    Run the bot.
    """
    application = Application.builder().token(token=bot_token).build()

    # Register command handlers
    application.add_handler(
        handler=CommandHandler(
            command="word",
            callback=handle_word,
        )
    )
    application.add_handler(
        handler=CommandHandler(
            command="help",
            callback=handle_help,
        )
    )
    application.add_handler(
        handler=CommandHandler(
            command="audio",
            callback=handle_audio,
        )
    )
    application.add_handler(
        handler=CommandHandler(
            command="web_word",
            callback=handle_web_word,
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
