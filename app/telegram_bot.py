import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from environs import Env

from app.main import get_anki_note_data, save_anki_note_to_list


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

env = Env()
env.read_env()

# Telegram bot token
TOKEN = env("TELEGRAM_TOKEN")

# File path to store Anki notes
ANKI_NOTES_FILE_PATH = env("ANKI_NOTES_FILE_PATH") or "anki_notes.txt"


logger = logging.getLogger(__name__)


async def handle_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Asynchronously handles a word update.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.

    Returns:
        None
    """
    args = context.args or []
    word = " ".join(args)
    message = update.message
    if not message:
        logger.error("No message provided.")
        return
    if word:
        await save_anki_note_to_list(word)
        msg = f"Anki note of {word=} saved successfully."
        logger.info(msg)
        await message.reply_text(msg)
        data = await get_anki_note_data(word)
        await message.reply_text(data.pretty_print())
    else:
        msg = "Please provide a word to create an Anki note."
        logger.info(msg)
        await message.reply_text(msg)


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Asynchronously handles a word update.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.

    Returns:
        None
    """
    message = update.message
    if not message:
        logger.error("No message provided.")
        return
    msg = (
        "Commands:\n"
        "/help: Provides help of the bot.\n/word: Creates an Anki note content and"
        "set the Note to the queue to save in Anki."
    )
    logger.info(msg)
    await message.reply_text(msg)


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("word", handle_word))
    application.add_handler(CommandHandler("help", handle_help))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
