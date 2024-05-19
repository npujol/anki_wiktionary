import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from pathlib import Path

from app.main import (
    generate_audio,
    get_anki_note_data,
    save_anki_note_to_list,
    send_card_using_anki_web,
)


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
    if not word:
        msg = "Please provide a word to create an Anki note."
        logger.info(msg)
        await message.reply_text(msg)
        return

    note = await send_card_using_anki_web(word)
    if note is None:
        msg = "Anki note could not be created."
        logger.error(msg)
        await message.reply_text(msg)
        return

    logger.info("Anki note created successfully.")
    await message.reply_text(note.pretty_print())
    if note is not None and note.audio and note.audio[0]:
        filepath = Path(__file__).parent.parent / f"files/{word}.mp3"
        await message.reply_audio(filepath)
        filepath.unlink()


# --------------------------------------------
# From the examples
# --------------------------------------------

# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text(
        "Start handler, Choose a route", reply_markup=reply_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(
        text="Start handler, Choose a route", reply_markup=reply_markup
    )
    return START_ROUTES


async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("3", callback_data=str(THREE)),
            InlineKeyboardButton("4", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="First CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return START_ROUTES


async def two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Second CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return START_ROUTES


async def three(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons. This is the end point of the conversation."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Yes, let's do it again!", callback_data=str(ONE)),
            InlineKeyboardButton("Nah, I've had enough ...", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Third CallbackQueryHandler. Do want to start over?",
        reply_markup=reply_markup,
    )
    # Transfer to conversation state `SECOND`
    return END_ROUTES


async def four(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Fourth CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return START_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    return ConversationHandler.END
