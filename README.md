# anki_wiktionary
A small project aimed at generating Anki notes using Wiktionary. Leveraging the power of [Anki](https://apps.ankiweb.net/), this initiative taps into a unique source: a Telegram bot. By harnessing the vast linguistic knowledge contained within the Telegram bot, we can create a comprehensive set of Anki notes that will help users expand their vocabulary and improve their language skills.

## Dependencies
- Anki running in the background

## Installation

1. Clone the project
    ```bash
    git clone git@github.com:npujol/anki_wiktionary.git
    ```
2. Move to the project directory
    ```bash
    cd anki_wiktionary
    ```
3. Install dependencies
    ```bash
    poetry install
    ```

## Environment Variables

Set the following environment variables:

```
TELEGRAM_TOKEN="your_telegram_bot_token"
ANKI_NOTES_FILE_PATH="anki_notes.txt"
ANKI_USER="your@email.com"
ANKI_PASS="a_password"
BROWSER_PATH="/usr/bin/webdriver"
BROWSERDRIVER_PATH="/usr/bin/chromedriver"
FILES_PATH="files"
```

| Name                   | Description                                  |
|------------------------|----------------------------------------------|
| `TELEGRAM_TOKEN`       | Telegram bot token.                          |
| `ANKI_NOTES_FILE_PATH` | File path to store Anki notes.               |
| `ANKI_USER`            | Anki username.                               |
| `ANKI_PASS`            | Anki password.                               |
| `BROWSER_PATH`         | Path to browser.                             |
| `BROWSERDRIVER_PATH`    | Path to Chromedriver (optional).             |
| `FILES_PATH`           | Path to save audio files.                    |

## How to Create a Bot with BotFather on Telegram

Follow these steps:

1. Open Telegram and search for `BotFather` in the search bar.
2. Start a chat with BotFather by clicking on it and then click on the `Start` button or send a `/start` message.
3. Send the `/newbot` command to create a new bot. BotFather will ask you to choose a name for your bot.
4. After choosing a name, BotFather will ask you to choose a username for your bot. This username should end with "bot" and be unique.
5. Once you've chosen a username, BotFather will provide you with a token. This token is your bot's API token, which you'll use to authenticate your bot when interacting with the Telegram Bot API.

__Note__: Copy the token provided by BotFather and save it securely. Do not share this token with anyone else as it grants access to your bot.

## Project Commands

- Running the Telegram bot in the background:
    ```bash
    python app/telegram_bot/main.py
    ```
- Generating notes using the information from the environment variable `ANKI_NOTES_FILE_PATH`:
    ```bash
    python app/main.py
    ```
- Starting a web server to serve audio files:
    ```bash
    python app/server.py
    ```

## Telegram Bot Commands

- `/help`: Provides help for the bot.
- `/word`: Creates an Anki note content and saves the word into the `ANKI_NOTES_FILE_PATH` file to be imported into Anki.
- `/web_word`: Creates an Anki note and sends it to Anki using Selenium. Note: This option cannot send audio files.
- `/audio`: Creates audio from a given text.

## Compiling and Running Using Nix

1. Build the bot:
    ```bash
    nix build
    ```
2. Run the bot:
    ```bash
    ./result/bin/bot
    ```

## Compiling and Running Using Docker

### Requirements

- [Docker](https://docs.docker.com/engine/install/)

### Steps

1. Build the Docker image:
    ```bash 
    docker build -t telegram-bot-anki .
    ```
2. Run the Docker container:
    ```bash
    docker run -e FILES_PATH=<PATH> -e ANKI_PASS=<PASSWORD> -e ANKI_USER=<USERNAME> -e TELEGRAM_TOKEN=<TELEGRAM_TOKEN> -e ANKI_NOTES_FILE_PATH=<ANKI_NOTES_FILE_PATH> telegram-bot-anki
    ```

Make sure to replace placeholders like `<PATH>`, `<PASSWORD>`, `<USERNAME>`, `<TELEGRAM_TOKEN>`, and `<ANKI_NOTES_FILE_PATH>` with your actual values.