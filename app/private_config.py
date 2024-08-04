from pathlib import Path

from environs import Env

env = Env()
env.read_env(override=True)

# Path to Browser binary to be used for selenium webdriver
browser_binary_location: str = env("BROWSER_PATH")  # type: ignore
browser_driver_binary: str = env("BROWSERDRIVER_PATH") or "/usr/bin/webdriver"  # type: ignore

files_path: str = env("FILES_PATH", default="files")  # type: ignore
working_path: Path = Path(files_path)  # type: ignore
working_path.mkdir(parents=True, exist_ok=True)

# Anki credentials and settings
anki_note_file_path: str = env("ANKI_NOTES_FILE_PATH", default="anki_notes.txt")  # type: ignore
anki_username: str = env.str("ANKI_USER", default=None)  # type: ignore
anki_password: str = env.str("ANKI_PASS", default=None)  # type: ignore
anki_deck_name: str = env.str("ANKI_DECK_NAME", default="Mein Deutsch")  # type: ignore

# Telegram bot credentials
bot_token: str = env.str("TELEGRAM_TOKEN", default=None)  # type: ignore

# Ollama server url
ollama_server_url: str = env.str("OLLAMA_URL", default="http://127.0.0.1:11434")  # type: ignore
