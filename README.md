# anki_wiktionary
A small project to create Anki notes from the Wiktionary database.

# Dependencies
- Anki running in the background
- Poetry

# Installation

- Clone the project
    ```bash
    git clone git@github.com:npujol/anki_wiktionary.git
    ```
- Move to project
    ```bash
    cd anki_wiktionary
    ```
- Install dependencies
    ```bash
    poetry install
    ```

# Environment variables
```
TELEGRAM_TOKEN="your_telegram_bot_token"
ANKI_NOTES_FILE_PATH="anki_notes.txt"
```


# Create a bot with __BotFather__ on Telegram. 

Follow these following steps:

1. Open Telegram and search for __BotFather__ in the search bar.
2. Start a chat with BotFather by clicking on it and then click on the __Start__ button or send a `/start` message.
3. Send the `/newbot` command to create a new bot. BotFather will ask you to choose a name for your bot.
4. After choosing a name, BotFather will ask you to choose a username for your bot. This username should end with "bot" and be unique.
5. Once you've chosen a username, BotFather will provide you with a token. This token is your bot's API token, which you'll use to authenticate your bot when interacting with the Telegram Bot API.

__Note__: Copy the token provided by BotFather and save it securely. Do not share this token with anyone else as it grants access to your bot.


# Commands

- Running telegram bot
    ```bash
    python app/telegram_bot.py
    ```

- Running notes generation
    ```bash
    python app/main.py
    ```

## Bot command
- `/word`: Creates an Anki note content and set the Note to the queue to save in Anki.
- `/help`: Provides help of the bot.
