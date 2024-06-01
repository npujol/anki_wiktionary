from pathlib import Path

from environs import Env

env = Env()
env.read_env(override=True)

# Path to Browser binary to be used for selenium webdriver
browser_binary_location: str = env("BROWSER_PATH")
browser_driver_binary: str = env("BROWSERDRIVER_PATH") or "/usr/bin/webdriver"

files_path: str = env("FILES_PATH", default="files")
working_path: Path = Path(files_path)
working_path.mkdir(parents=True, exist_ok=True)

# Anki credentials and settings
anki_note_file_path = env("ANKI_NOTES_FILE_PATH", default="anki_notes.txt")
anki_username = env.str("ANKI_USER", default=None)
anki_password = env.str("ANKI_PASS", default=None)


# Telegram bot credentials
bot_token = env.str("TELEGRAM_TOKEN", default=None)
