import logging

from telegram import Message, Update
from telegram.ext import (
    CallbackContext,
    ContextTypes,
)

from app.main import (
    generate_audio,
    get_anki_note_data,
    save_anki_note_to_list,
    send_card_using_anki_web,
)
from app.private_config import working_path

logger = logging.getLogger(name=__name__)


async def handle_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /word command. Create an Anki note for the given word.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.
    """
    args = context.args or []
    word = " ".join(args)
    message = update.message
    if not message:
        logger.error(msg="No message provided.")
        return
    if word:
        await _handle_word(word=word, message=message)
    else:
        msg = "Provide the word to create the anki note:"
        logger.info(msg=msg)
        await message.reply_text(text=msg)


async def _handle_word(word: str, message: Message) -> None:
    """
    Handle the processing of a word, saving it as an Anki note, and replying
    with the note data.

    Args:
        word (str): The word to process.
        message (Message): The Telegram message object.
    """
    await save_anki_note_to_list(word=word)
    msg = f"Anki note for '{word}' saved successfully."
    logger.info(msg=msg)
    await message.reply_text(text=msg)
    note = await get_anki_note_data(word=word)
    if not note:
        await message.reply_text(text="Anki note could not be created.")
        return
    await message.reply_text(text=note.pretty_print())
    if note.audio and note.audio[0]:
        filepath = working_path / f"{word}.mp3"
        await message.reply_audio(audio=filepath)
        filepath.unlink()


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /audio command. Create audio from the provided text.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.
    """
    args = context.args or []
    text = " ".join(args)
    message = update.message
    if not message:
        logger.error(msg="No message provided.")
        return
    if text:
        filepath = await generate_audio(text=text)
        await message.reply_audio(audio=filepath)
        filepath.unlink()
    else:
        msg = "Please provide a sentence to create audio."
        logger.info(msg=msg)
        await message.reply_text(text=msg)


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /help command. Provide information about available commands.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.
    """
    message = update.message
    if not message:
        logger.error(msg="No message provided.")
        return
    msg = (
        "Commands:\n"
        "/help: Provides help for the bot.\n"
        "/word: Creates an Anki note for a word.\n"
        "/audio: Creates audio from a text.\n"
        "/web_word: Creates a deck and sends it to the web browser."
    )
    logger.info(msg=msg)
    await message.reply_text(text=msg)


async def handle_web_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /web_word command. Create an Anki note and send it to AnkiWeb.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.
    """
    args = context.args or []
    word = " ".join(args)
    message = update.message
    if not message:
        logger.error(msg="No message provided.")
        return
    if not word:
        msg = "Please provide a word to create an Anki note."
        logger.info(msg=msg)
        await message.reply_text(text=msg)
        return

    note = await send_card_using_anki_web(word=word)
    if not note:
        msg = "Anki note could not be created."
        logger.error(msg=msg)
        await message.reply_text(text=msg)
        return

    logger.info(msg="Anki note created successfully.")
    await message.reply_text(text=note.pretty_print())
    if note.audio and note.audio[0]:
        filepath = working_path / f"{word}.mp3"
        await message.reply_audio(audio=filepath)
        filepath.unlink()


async def handle_text_without_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handle text messages without a command. Treat them as if they were /word commands.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.
    """
    if not update.message:
        logger.error(msg="No message provided.")
        return
    word = update.message.text
    if word:
        await handle_word(update=update, context=context)


async def unsupported_message_handle(update: Update, context: CallbackContext) -> None:
    """
    Handle unsupported message types.

    Args:
        update (Update): The update object.
        context (CallbackContext): The context object.
    """
    error_text = "I don't know how to process other inputs. I only work with text."
    logger.error(msg=error_text)
    if update.message:
        await update.message.reply_text(text=error_text)


async def message_handle(update: Update, context: CallbackContext) -> None:
    """
    Handle messages, defaulting to the /web_word command.

    Args:
        update (Update): The update object.
        context (CallbackContext): The context object.
    """
    if not update.message:
        return
    word = update.message.text
    if not word:
        await unsupported_message_handle(update=update, context=context)
        return

    await update.message.reply_text(text="Using the default command /web_word")
    note = await send_card_using_anki_web(word=word)
    if not note:
        msg = "Anki note could not be created."
        logger.error(msg=msg)
        await update.message.reply_text(text=msg)
        return

    logger.info(msg="Anki note created successfully.")
    await update.message.reply_text(text=note.pretty_print())
    if note.audio and note.audio[0]:
        filepath = working_path / f"{word}.mp3"
        await update.message.reply_audio(audio=filepath)
        filepath.unlink()
