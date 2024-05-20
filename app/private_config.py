from environs import Env

env = Env()
env.read_env(override=True)

# Path to Chrome binary to be used for selenium webdriver
# Docs: https://www.selenium.dev/documentation/webdriver/browsers/chrome/
chrome_binary_location = env("BROWSER_PATH") or "/usr/bin/webdriver"
