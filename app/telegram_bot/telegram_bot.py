import logging

from environs import Env
from telegram import BotCommand, Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from app.telegram_bot.handlers import (
    handle_audio,
    handle_help,
    handle_web_word,
    handle_word,
    message_handle,
    unsupport_message_handle,
)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
env = Env()
env.read_env()
TOKEN = env("TELEGRAM_TOKEN")
ANKI_NOTES_FILE_PATH = env("ANKI_NOTES_FILE_PATH") or "anki_notes.txt"


async def post_init(application: Application):
    """
    Set bot commands after initializing the bot.

    Args:
        application (Application): The application object.
    """
    await application.bot.set_my_commands(
        [
            BotCommand("/word", "Create an Anki note for a word"),
            BotCommand("/help", "Show help message"),
            BotCommand("/audio", "Create audio from text"),
            BotCommand("/web_word", "Create an Anki note and send it to AnkiWeb"),
        ]
    )


def main() -> None:
    """
    Run the bot.
    """
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("word", handle_word))
    application.add_handler(CommandHandler("help", handle_help))
    application.add_handler(CommandHandler("audio", handle_audio))
    application.add_handler(CommandHandler("web_word", handle_web_word))

    # Register message handlers
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message_handle)
    )
    application.add_handler(
        MessageHandler(
            filters.VIDEO & ~filters.COMMAND & filters.PHOTO,
            unsupport_message_handle,
        )
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
