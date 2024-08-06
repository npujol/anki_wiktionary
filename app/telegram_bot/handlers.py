import logging
from pathlib import Path
from typing import Any

from telegram import Message, Update
from telegram.ext import (
    ContextTypes,
)

from app.main import (
    generate_audio,
    get_anki_note_data,
    save_anki_note_to_list,
    send_card_using_anki_web,
)
from app.private_config import working_path
from app.serializers import CustomNote

logger: logging.Logger = logging.getLogger(name=__name__)


async def handle_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /word command. Create an Anki note for the given word.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.
    """
    logger.error(msg="Starting handle_word function.")
    args: list[str] = context.args or []
    word: str = " ".join(args)
    message: Message | None = update.message
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
    msg: str = f"Anki note for '{word}' saved successfully."
    logger.info(msg=msg)
    await message.reply_text(text=msg)
    note: CustomNote | None = await get_anki_note_data(word=word)
    if not note:
        await message.reply_text(text="Anki note could not be created.")
        return
    await message.reply_text(text=note.pretty_print())
    if note.audio and note.audio[0]:
        filepath: Path = working_path / f"{word}.mp3"
        await message.reply_audio(audio=filepath)
        if filepath.exists():
            filepath.unlink()


async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /audio command. Create audio from the provided text.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.
    """
    logger.error(msg="Starting handle_audio function.")

    args: list[str] = context.args or []
    text: str = " ".join(args)
    message: Message | None = update.message
    if not message:
        logger.error(msg="No message provided.")
        return
    if text:
        filepath: Path = await generate_audio(text=text)
        await message.reply_audio(audio=filepath)
        if filepath.exists():
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
    logger.error(msg="Starting handle_help function.")

    message: Message | None = update.message
    if not message:
        logger.error(msg="No message provided.")
        return
    msg = (
        "Commands:\n"
        "/help: Provides help for the bot.\n"
        "/w: Creates an Anki note for a word.\n"
        "/a: Creates audio from a text.\n"
        "/ww: Creates a deck and sends it to the web browser."
        "/d: Creates an Anki note from duden.\n"
        "/v: Creates an Anki note from verben.\n"
    )
    logger.info(msg=msg)
    await message.reply_text(text=msg)


async def handle_web_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /w command. Create an Anki note and send it to AnkiWeb.

    Args:
        update (Update): The update object.
        context (ContextTypes.DEFAULT_TYPE): The context object.
    """
    logger.error(msg="Starting handle_web_word function.")

    args: list[str] = context.args or []
    word: str = " ".join(args)
    message: Message | None = update.message
    if not message:
        logger.error(msg="No message provided.")
        return
    if not word:
        msg = "Please provide a word to create an Anki note."
        logger.info(msg=msg)
        await message.reply_text(text=msg)
        return

    note: CustomNote | None = await send_card_using_anki_web(word=word)
    if not note:
        msg = "Anki note could not be created."
        logger.error(msg=msg)
        await message.reply_text(text=msg)
        return

    logger.info(msg="Anki note created successfully.")
    await message.reply_text(text=note.pretty_print())
    if note.audio and note.audio[0]:
        filepath: Path = working_path / f"{word}.mp3"
        await message.reply_audio(audio=filepath)
        if filepath.exists():
            filepath.unlink()


async def handle_verben_word(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(msg="Starting handle_verben_word function.")
    args: list[str] = context.args or []
    word: str = " ".join(args)
    message: Message | None = update.message
    if not message:
        logger.error(msg="No message provided.")
        return
    if not word:
        msg = "Please provide a word to create an Anki note."
        logger.info(msg=msg)
        await message.reply_text(text=msg)
        return

    note: CustomNote | None = await send_card_using_anki_web(
        word=word, processor_name="verben", model_name="Basic"
    )
    if not note:
        msg = "Anki note could not be created."
        logger.error(msg=msg)
        await message.reply_text(text=msg)
        return

    logger.info(msg="Anki note created successfully.")
    await message.reply_text(text=note.pretty_print())
    if note.audio and note.audio[0]:
        filepath: Path = working_path / f"{word}.mp3"
        await message.reply_audio(audio=filepath)
        if filepath.exists():
            filepath.unlink()


async def handle_duden_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(msg="Starting handle_duden_word function.")
    args: list[str] = context.args or []
    word: str = " ".join(args)
    message: Message | None = update.message
    if not message:
        logger.error(msg="No message provided.")
        return
    if not word:
        msg = "Please provide a word to create an Anki note."
        logger.info(msg=msg)
        await message.reply_text(text=msg)
        return

    note: CustomNote | None = await send_card_using_anki_web(
        word=word, processor_name="duden", model_name="Basic_"
    )
    if not note:
        msg = "Anki note could not be created."
        logger.error(msg=msg)
        await message.reply_text(text=msg)
        return

    logger.info(msg="Anki note created successfully.")
    await message.reply_text(text=note.pretty_print())
    if note.audio and note.audio[0]:
        filepath: Path = working_path / f"{word}.mp3"
        await message.reply_audio(audio=filepath)
        if filepath.exists():
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
    logger.info(msg="Starting handle_text_without_command function.")
    if not update.message:
        logger.error(msg="No message provided.")
        return
    word: str | None = update.message.text
    if word:
        await handle_word(update=update, context=context)


async def unsupported_message_handle(update: Update, *args: Any, **kwargs: Any) -> None:
    """
    Handle unsupported message types.

    Args:
        update (Update): The update object.
        context (CallbackContext): The context object.
    """
    logger.info(msg="Starting unsupported_message_handle function.")
    error_text = "I don't know how to process other inputs. I only work with text."
    logger.error(msg=error_text)
    if update.message:
        await update.message.reply_text(text=error_text)


async def message_handle(
    update: Update, context: Any, *args: Any, **kwargs: Any
) -> None:
    """
    Handle messages, defaulting to the /web_word command.

    Args:
        update (Update): The update object.
        context (CallbackContext): The context object.
    """
    logger.info(msg="Starting message_handle function.")
    if not update.message:
        return
    word: str | None = update.message.text
    if not word:
        await unsupported_message_handle(update=update, context=context)
        return

    await update.message.reply_text(text="Using the default command /web_word")
    note: CustomNote | None = await send_card_using_anki_web(word=word)
    if not note:
        msg = "Anki note could not be created."
        logger.error(msg=msg)
        await update.message.reply_text(text=msg)
        return

    logger.info(msg="Anki note created successfully.")
    await update.message.reply_text(text=note.pretty_print())
    if note.audio and note.audio[0]:
        filepath: Path = working_path / f"{word}.mp3"
        await update.message.reply_audio(audio=filepath)
        if filepath.exists():
            filepath.unlink()
