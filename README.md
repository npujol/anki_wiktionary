# anki_wiktionary
A small project aims to generate Anki notes using Wiktionary. Leveraging the power of  [Anki](https://apps.ankiweb.net/), this initiative taps into a unique source: a telegram bot. By harnessing the vast linguistic knowledge contained within the Telegram bot, we can create a comprehensive set of Anki notes that will help users expand their vocabulary and improve their language skills.

# Dependencies
- Anki running in the background

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
ANKI_USER="your@email.com"
ANKI_PASS="a_password"
BROWSER_PATH="/usr/bin/webdriver"
CHROMEDRIVER_PATH="/usr/bin/chromedriver"
FILES_PATH="files"
```

|Name|Description|
|---|---|
|`TELEGRAM_TOKEN`|Telegram bot token.|
|`ANKI_NOTES_FILE_PATH`|File path to store Anki notes.|
|`ANKI_USER`|Anki username.|
|`ANKI_PASS`|Anki password.|
|`BROWSER_PATH`| Path to browser.|
|`CHROMEDRIVER_PATH`| Path to chromedriver. Optional |
|`FILES_PATH`| Path to save audio files.|


**How to create a bot with __BotFather__ on Telegram?**
========================================================
Follow these following steps:

1. Open Telegram and search for __BotFather__ in the search bar.
2. Start a chat with BotFather by clicking on it and then click on the __Start__ button or send a `/start` message.
3. Send the `/newbot` command to create a new bot. BotFather will ask you to choose a name for your bot.
4. After choosing a name, BotFather will ask you to choose a username for your bot. This username should end with "bot" and be unique.
5. Once you've chosen a username, BotFather will provide you with a token. This token is your bot's API token, which you'll use to authenticate your bot when interacting with the Telegram Bot API.

__Note__: Copy the token provided by BotFather and save it securely. Do not share this token with anyone else as it grants access to your bot.


# Project commands

- Running telegram bot in the background
```bash
python app/telegram_bot.py
```

- Running notes generation using the information from the environment variable `ANKI_NOTES_FILE_PATH`.          
```bash
    python app/main.py
```

- Start a web server to serve audios
```bash
python app/server.py
```

## Telegram bot command
- `/help`: Provides help of the bot.
- `/word`: Creates an Anki note content and set the Word into the `ANKI_NOTES_FILE_PATH` file to be saved in Anki.
- `/web_word`: Create an Anki note and send it into Anki using Selenium. This option had the limitation that it cannot send the audio file.
- `/audio`: Creates audio from a given text.


## Compile and running using Nix


1. Step 1: Build the bot

```bash
nix build
```

2. Step 2: Running the bot
```bash
./result/bin/bot
```