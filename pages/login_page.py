import time
from dotenv import load_dotenv
import os
from pages.base_page import BasePage
from locators import web_locators as l


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_login_page(self, url: str):
        self.driver.get(url)
        self.wait_for_page_to_load(url)

    def fill_details_login(self):
        load_dotenv()
        self.type_to_element(l.password_field_login_page, os.getenv("LOGIN_PASSWORD"))
        self.click_element(l.enter_button_login_page)


