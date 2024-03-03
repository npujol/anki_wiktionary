# Telegram bot token
TOKEN = "7012446974:AAHvqbUjQseYp1KV1EIvB_8Hds49UyEEp5Y"

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import datetime

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# File path to store Anki notes
ANKI_NOTES_FILE_PATH = "anki_notes.txt"


# Function to create an Anki note
async def create_anki_note(word: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ANKI_NOTES_FILE_PATH, "a") as file:
        file.write(f"{timestamp}: {word}\n")
    print(f"Anki note created: {timestamp}: {word}")


# Command handler for the bot
async def handle_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    word = " ".join(context.args)
    if word:
        await create_anki_note(word)
        await update.message.reply_text("Anki note created successfully.")
    else:
        await update.message.reply_text("Please provide a word to create an Anki note.")


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("word", handle_word))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
