from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pyvirtualdisplay import Display  # type: ignore
import traceback
from selenium.webdriver.chrome.service import Service
from app.serializers import CustomNote
from private_config import chrome_binary_location

WINDOW_SIZE = (800, 600)


class WebAnkiConnector:
    url = "https://ankiweb.net/account/login"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def start(self):
        """Start the browser with the given credentials"""
        # Start the virtual display
        self.display = Display(visible=False, size=WINDOW_SIZE)
        self.display.start()
        # Create the Chrome browser service
        service = Service(chrome_binary_location)
        # Set up browser options
        options = webdriver.ChromeOptions()
        options.add_argument(f"--window-size={WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Start the browser
        self.driver = webdriver.Chrome(service=service, options=options)

        if self.driver is None:
            raise Exception("Failed to start Chrome")

        self._login_into_anki(self.username, self.password)

    def close(self):
        """Shut down the browser"""
        self.driver.quit()
        self.display.stop()

    def send_card(self, custom_note: CustomNote, tags: list[str]) -> bool:
        """Send a card to Anki with the given fields from a CustomNote and tags"""
        try:
            self._click_add_tab()
            self._wait_for_elements_to_appear()
            self._fill_tags(tags)
            self._fill_fields(custom_note)
            self._click_add_button()
            return True
        except Exception as e:
            print(traceback.format_exc())
            raise e from e

    def _login_into_anki(self, username: str, password: str):
        try:
            self.driver.set_window_size(*WINDOW_SIZE)
            self.driver.get(self.url)
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//input[@autocomplete="username"]')
                )
            )
            usr_box = self.driver.find_element(
                "xpath", '//input[@autocomplete="username"]'
            )
            usr_box.send_keys(username)
            pass_box = self.driver.find_element(
                "xpath", '//input[@autocomplete="current-password"]'
            )
            pass_box.send_keys("{}\n".format(password))
        except Exception as e:
            print(traceback.format_exc())
            raise e from e

    def _click_add_tab(self):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="navbarSupportedContent"]/ul[1]/li[2]/a')
            )
        )
        self.driver.find_element(
            "xpath", '//*[@id="navbarSupportedContent"]/ul[1]/li[2]/a'
        ).click()

    def _wait_for_elements_to_appear(self):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div/main/form/button")
            )
        )

    def _fill_tags(self, tags: list[str]):
        if tags:
            tag_input = self.driver.find_element(
                "xpath", "/html/body/div/main/form/div[last()]/div/input"
            )
            for tag in tags:
                tag_input.send_keys(tag)
                tag_input.send_keys(",")

    def _fill_fields(self, custom_note: CustomNote):
        audio_file_xpath = None

        for k, (f, v) in enumerate(
            custom_note.fields.model_dump(mode="python").items(), start=1
        ):
            if f == "audio":
                audio_file_xpath = f"/html/body/div/main/form/div[{k}]/div/div"
                continue
            if v is None:
                continue
            field_div = self.driver.find_element(
                "xpath", f"/html/body/div/main/form/div[{k}]/div/div"
            )
            field_div.send_keys(v)

        if audio_file_xpath:
            # TODO web version doesn't support uploading audio files
            pass

    def _click_add_button(self):
        add_button = self.driver.find_element(
            "xpath", "/html/body/div/main/form/button"
        )
        add_button.click()
