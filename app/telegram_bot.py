import logging
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from environs import Env

from app.main import (
    generate_audio,
    get_anki_note_data,
    save_anki_note_to_list,
    send_card_web,
)


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
        note = await get_anki_note_data(word)
        if not note:
            await message.reply_text("Anki note could not be created.")
            return
        await message.reply_text(note.pretty_print())
        if note is not None and note.audio and note.audio[0]:
            filepath = Path(__file__).parent.parent / f"files/{word}.mp3"
            await message.reply_audio(filepath)
            filepath.unlink()
    else:
        msg = "Please provide a word to create an Anki note."
        logger.info(msg)
        await message.reply_text(msg)


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args or []
    text = " ".join(args)
    message = update.message
    if not message:
        logger.error("No message provided.")
        return
    if text:
        filepath = await generate_audio(text)
        await message.reply_audio(filepath)
        filepath.unlink()
    else:
        msg = "Please provide a sentence to create audio."
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
        "set the Note to the queue to save in Anki.\n/audio: Creates audio from a text"
        "\n/web_word: create deck and send it to web browser"
    )
    logger.info(msg)
    await message.reply_text(msg)


async def handle_web_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        note = send_card_web(word)
        if not note:
            await message.reply_text("Anki note could not be created.")
            return
        await message.reply_text(note.pretty_print())
        if note is not None and note.audio and note.audio[0]:
            filepath = Path(__file__).parent.parent / f"files/{word}.mp3"
            await message.reply_audio(filepath)
            filepath.unlink()
    else:
        msg = "Please provide a word to create an Anki note."
        logger.info(msg)
        await message.reply_text(msg)


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("word", handle_word))
    application.add_handler(CommandHandler("help", handle_help))
    application.add_handler(CommandHandler("audio", handle_audio))
    application.add_handler(CommandHandler("web_word", handle_web_word))
    # TODO IPA, translation
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
