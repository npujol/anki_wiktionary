from pathlib import Path

from environs import Env

env = Env()
env.read_env(override=True)

# Path to Chrome binary to be used for selenium webdriver
# Docs: https://www.selenium.dev/documentation/webdriver/browsers/chrome/
browser_binary_location: str = env("BROWSER_PATH")
browser_driver_binary: str = env("BROWSERDRIVER_PATH") or "/usr/bin/webdriver"

files_path: str = env("FILES_PATH") or "files"
working_path: Path = Path(files_path)
working_path.mkdir(parents=True, exist_ok=True)
