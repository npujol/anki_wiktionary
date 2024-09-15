import traceback
from typing import Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.private_config import browser_binary_location, browser_driver_binary
from app.serializers import CustomNote

from .errors import BrowserNotFoundError

TIMEOUT = 150


class AnkiWebConnector:
    login_url: str = "https://ankiweb.net/account/login"

    def __init__(self, username: str, password: str) -> None:
        self.username: str = username
        self.password: str = password

    def start(self) -> None:
        """Start the browser with the given credentials"""
        # Start the virtual display
        # Create the Browser browser service
        service = Service(executable_path=browser_driver_binary)
        # Set up browser options
        options = webdriver.FirefoxOptions()
        options.add_argument(  # type: ignore
            argument="--headless"
        )  # Run in headless mode
        if browser_binary_location:
            options.binary_location = browser_binary_location
        # Start the browser
        self.driver = webdriver.Firefox(service=service, options=options)
        if self.driver is None:  # type: ignore
            raise BrowserNotFoundError("Failed to start the browser")

        self._login_into_anki(username=self.username, password=self.password)

    def close(self) -> None:
        """Shut down the browser"""
        self.driver.quit()

    def send_card(
        self,
        custom_note: CustomNote,
        tags: list[str],
        card_type: str = "Basic_",
    ) -> bool:
        """
        Send a card to Anki with the given fields from a CustomNote and tags
        Args:
            custom_note (CustomNote): The note to send to Anki
            tags (list[str]): The tags to apply to the card
            card_type (str): The type of card to send
        Returns:
            bool: Whether the card was sent successfully
        """
        try:
            self._click_add_tab()
            self._wait_for_elements_to_appear()
            self._select_card_type(card_type=card_type)
            self._fill_tags(tags=tags)
            self._fill_fields(custom_note=custom_note)
            self._click_add_button()
            return True
        except Exception as e:
            print(traceback.format_exc())
            raise e from e

    def _login_into_anki(self, username: str, password: str) -> None:
        try:
            self.driver.get(url=self.login_url)
            WebDriverWait(driver=self.driver, timeout=TIMEOUT).until(
                method=EC.visibility_of_element_located(
                    locator=(By.XPATH, '//input[@autocomplete="username"]')
                )
            )
            usr_box: Any = self.driver.find_element(
                by="xpath", value='//input[@autocomplete="username"]'
            )
            usr_box.send_keys(username)
            pass_box: Any = self.driver.find_element(
                by="xpath", value='//input[@autocomplete="current-password"]'
            )
            pass_box.send_keys(password)
            pass_box.send_keys(Keys.ENTER)
        except Exception:
            print(traceback.format_exc())
            raise

    def _select_card_type(self, card_type: str = "Basic_") -> None:
        wait = WebDriverWait(driver=self.driver, timeout=TIMEOUT)
        input_element: Any = wait.until(
            method=EC.presence_of_element_located(
                locator=(By.CSS_SELECTOR, "input.svelte-apvs86")
            )
        )

        # Click on the input element to activate the dropdown (if necessary)
        input_element.click()
        input_element.send_keys(card_type)
        input_element.send_keys(Keys.ENTER)

    def _click_add_tab(self) -> None:
        WebDriverWait(driver=self.driver, timeout=TIMEOUT).until(
            method=EC.visibility_of_element_located(
                locator=(By.XPATH, '//*[@id="navbarSupportedContent"]/ul[1]/li[2]/a')
            )
        )
        self.driver.find_element(
            by="xpath", value='//*[@id="navbarSupportedContent"]/ul[1]/li[2]/a'
        ).click()

    def _wait_for_elements_to_appear(self) -> None:
        WebDriverWait(driver=self.driver, timeout=TIMEOUT).until(
            method=EC.visibility_of_element_located(
                locator=(By.XPATH, "/html/body/div/main/form/button")
            )
        )

    def _fill_tags(self, tags: list[str]) -> None:
        if tags:
            tag_input: Any = self.driver.find_element(
                by="xpath", value="/html/body/div/main/form/div[last()]/div/input"
            )
            for tag in tags:
                tag_input.send_keys(tag)
                tag_input.send_keys(",")

    def _fill_fields(self, custom_note: CustomNote) -> None:
        audio_file_xpath: str | None = None
        if custom_note.fields is None:
            return

        for k, (f, v) in enumerate(
            iterable=custom_note.fields.model_dump(mode="python").items(), start=1
        ):
            if f == "audio":
                audio_file_xpath = f"/html/body/div/main/form/div[{k}]/div/div"
                continue

            if v is None:
                continue

            field_div: Any = self.driver.find_element(
                by="xpath", value=f"/html/body/div/main/form/div[{k}]/div/div"
            )
            self.driver.execute_script(  # type: ignore
                "arguments[0].innerHTML = arguments[1];",
                field_div,
                v,
            )
            # Workaround: to activate the upload button
            field_div.send_keys(" ")

        if audio_file_xpath:
            # TODO web version doesn't support uploading audio files
            pass

    def _click_add_button(self) -> None:
        add_button: Any = self.driver.find_element(
            by="xpath", value="/html/body/div/main/form/button"
        )
        add_button.click()
