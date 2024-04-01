from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from app.private_config import chrome_binary_location

import time
import traceback


import os

from app.serializers import CustomNote


class WebAnkiConnector:
    url = "https://ankiweb.net/account/login"

    def __init__(self, username: str, password: str):
        self.last_access = time.time()

        # Setup Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = chrome_binary_location
        self.driver = webdriver.Chrome()
        if self.driver is None:
            raise Exception("Failed to start Chrome")

        self._initialize_chrome(username, password)

    def _initialize_chrome(self, username, password):
        try:
            self.driver.set_window_size(1920, 1080)
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
            if not os.path.isfile("errors/screenshot_error.png"):
                self.driver.save_screenshot("errors/screenshot_error.png")
            raise e from e

    def send_card(self, custom_note: CustomNote, tags: list[str]) -> bool:
        try:
            self._click_add_tab()
            self._wait_for_elements_to_appear()
            self._fill_tags(tags)
            self._fill_fields(custom_note)
            self._click_add_button()
            return True
        except Exception as e:
            print(traceback.format_exc())
            if not os.path.isfile("screenshot_error.png"):
                self.driver.save_screenshot("screenshot_error.png")
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
