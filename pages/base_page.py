import os
from datetime import datetime
import re
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    __TIMEOUT = 90
    regex_for_xpath = r'^//.*'

    def __init__(self, driver):
        self.driver = driver

    def click_element(self, locator):
        """
        Clicks on a UI element.

        :param locator: Locator string
        """
        try:
            print(f"==> Clicking element {locator}")
            xpath_result = re.match(self.regex_for_xpath, locator)
            self.wait_for_element_to_be_visible(locator)
            if xpath_result is not None:
                element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, locator)))
            else:
                element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, locator)))
            element.click()
        except:
            print(f"Can't click on {locator}")

    def find_single_element(self, locator, timeout=__TIMEOUT):
        """
        Reads and returns text from a UI element.
        """
        try:
            xpath_result = re.match(self.regex_for_xpath, locator)
            if xpath_result is not None:
                return WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, locator)),
                    message=f"Element with Xpath '{locator}' was not found"
                )
            else:
                return WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, locator)),
                    message=f"Element with CSS '{locator}' was not found"
                )
        except:
            print(f"Can't find element: {locator}")

    def find_multiple_element(self, locator):
        xpath_result = re.match(self.regex_for_xpath, locator)
        if xpath_result is not None:
            return self.driver.find_elements(By.XPATH, locator)
        else:
            return self.driver.find_elements(By.CSS_SELECTOR, locator)

    def scroll_to_element(self, locator):
        """
        Scrolls the page until the element is in view.
        :param locator: Locator string
        """
        try:
            print(f"==> Scrolling to element {locator}")
            xpath_result = re.match(self.regex_for_xpath, locator)
            if xpath_result is not None:
                element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator)))
            else:
                element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))

            self.driver.execute_script("arguments[0].scrollIntoView();", element)
        except:
            print(f"Can't scroll to element: {locator}")

    def hover_over_element(self, locator):
        """
        Hovers the mouse over a UI element.

        :param locator: Locator string
        """
        try:
            print(f"==> Hover on element {locator}")
            xpath_result = re.match(self.regex_for_xpath, locator)
            if xpath_result is not None:
                element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator)))
            else:
                element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))

            ActionChains(self.driver).move_to_element(element).perform()
        except:
            print(f"Can't scroll to element: {locator}")

    def type_to_element(self, locator, text):
        """
        Types a given text into a UI element.

        :param locator: Locator string
        :param text: Text to input
        """
        try:
            print(f"==> Typing to element {locator} the text {text}")
            xpath_result = re.match(self.regex_for_xpath, locator)
            self.wait_for_element_to_be_visible(locator)
            if xpath_result is not None:
                element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, locator)))
            else:
                element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                                                                 locator)))

            element.clear()
            element.send_keys(text)
        except:
            print(f"Can't type to element: {locator} the text: {text}")

    def verify_url(self, expected_url):
        """
        Types a given text into a UI element.

        :param expected_url: String

        """
        current_url = self.driver.current_url
        assert expected_url == current_url, f"Expected {expected_url}, but got {current_url}"

    def press_enter(self, locator):
        print(f"==> Click 'Enter' in '{locator}'")
        self.find_single_element(self.driver, locator).send_keys(Keys.ENTER)

    def get_text(self, locator):
        try:
            for element_attr in ("text", "innerText", "value", "textContent"):
                text = self.find_single_element(locator).get_attribute(element_attr)
                if text and text != '':
                    break
            return text
        except:
            print(f"Can't get text on element: {locator}")

    def navigate_to_url(self, url):
        print(f"==> Navigate to URL {url}")
        self.driver.get(url)

    def wait_for_page_to_load(self, changed_url, timeout=__TIMEOUT):
        print(f"==> Waiting for page to load: \n{changed_url}")
        current_url = self.driver.current_url
        WebDriverWait(self.driver, timeout).until(EC.url_matches(changed_url),
                                                  message=f"Page was not changed to {changed_url}, "
                                                          f"the URL is {current_url}")

    def quit_driver(self):
        """
        Quits the WebDriver and closes the browser.
        """
        print("==> Quitting the driver and closing the browser")
        self.driver.quit()

    def refresh_page(self):
        """
        Refreshes the current page.
        """
        print("==> Refreshing the page")
        self.driver.refresh()

    def is_element_visible(self, locator, timeout=__TIMEOUT):
        """
        Verifies if a UI element is visible on the page.

        :param locator: Locator string
        :param timeout: Maximum time to wait for the element to be visible (default is 90 seconds)
        :return: True if the element is visible, False otherwise
        """
        print(f"==> Checking visibility of element {locator}")
        try:
            xpath_result = re.match(self.regex_for_xpath, locator)
            if xpath_result is not None:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((By.XPATH, locator))
                )
            else:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, locator))
                )
            return True
        except:
            return False

    def wait_for_element_to_be_invisible(self, locator, timeout=__TIMEOUT):
        """
        Waits for an element to become invisible.

        :param locator: Locator string
        :param timeout: Maximum time to wait for the element to be invisible (default is 90 seconds)
        :return: True if the element becomes invisible within the timeout, False otherwise
        """
        print(f"==> Waiting for element {locator} to be invisible")
        try:
            xpath_result = re.match(self.regex_for_xpath, locator)
            if xpath_result is not None:
                WebDriverWait(self.driver, timeout).until(
                    EC.invisibility_of_element_located((By.XPATH, locator))
                )
            else:
                WebDriverWait(self.driver, timeout).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, locator))
                )
            return True
        except:
            return False

    def wait_for_element_to_be_visible(self, locator, timeout=__TIMEOUT):
        """
        Waits for an element to become visible.

        :param locator: Locator string
        :param timeout: Maximum time to wait for the element to be visible (default is 90 seconds)
        :return: True if the element becomes visible within the timeout, False otherwise
        """
        print(f"==> Waiting for element {locator} to be visible")
        try:
            xpath_result = re.match(self.regex_for_xpath, locator)
            if xpath_result is not None:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((By.XPATH, locator))
                )
            else:
                WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, locator))
                )
            return True
        except:
            return False

    def take_screenshot(self, folder_path="screenshots"):
        """
        Takes a screenshot and saves it to the specified folder with a unique name.

        :param folder_path: The folder where the screenshot will be saved.
        """
        # Ensure the screenshots directory exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Create a unique file name with the current timestamp
        timestamp = datetime.now().strftime("Screenshot%d-%m-%Y-%H-%M-%S")
        file_path = os.path.join(folder_path, f"{timestamp}.png")

        # Take the screenshot and save it
        self.driver.save_screenshot(file_path)
        print(f"Screenshot saved to {file_path}")