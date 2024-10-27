import time

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.shopping_page import ShoppingPage
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from utils.common import check_test
from pages.shopping_page import BuyOption


def setup(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    if not headless:
        driver.maximize_window()
    return driver


@check_test
def ui_test():
    try:
        driver = setup()
        page = LoginPage(driver)
        # Navigate to the login page
        url = "https://drpt-external-dev.myshopify.com/password"
        page.navigate_to_login_page(url)
        page.fill_details_login()
        page.wait_for_page_to_load(page.driver.current_url)
        assert page.driver.current_url == 'https://drpt-external-dev.myshopify.com/'
        page = ShoppingPage(driver)
        product_name = 'Dropit Hamburger (QA Automation)'
        page.search_product(product_name)
        page.click_product(product_name)
        page.add_product_to_cart("2", BuyOption.ADD_TO_CART, "Medium")
        page.add_product_to_cart("1", BuyOption.ADD_TO_CART, "So large you can't eat it")

        product_name = 'Dropit Chips (QA Automation)'
        page.search_product(product_name)
        page.click_product(product_name)
        page.add_product_to_cart("2", BuyOption.ADD_TO_CART, "Large")
        page.add_product_to_cart("1", BuyOption.ADD_TO_CART, "Too much for you to handle")

        page.navigate_to_cart()

        page = CartPage(driver)
        # page.get_cart_list()
        page.click_on_checkout()
        page.get_and_verify_total_price("£56.99")
        return "Passed"
    except Exception as e:
        page.take_screenshot()
        raise e
