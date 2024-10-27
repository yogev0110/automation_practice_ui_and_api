from pages.base_page import BasePage
from locators import web_locators as l
from enum import Enum


class BuyOption(Enum):
    BUY_IT_NOW = 1,
    ADD_TO_CART = 2


class ShoppingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def search_product(self, product_name: str):
        self.click_element(l.search_button_shopping_page)
        self.type_to_element(l.search_field_shopping_page, product_name)

    def click_product(self, product_name: str):
        self.click_element(f'img[alt="{product_name}"]')
        text_title = self.get_text(l.product_title_shopping_page)
        assert text_title == product_name, f"==> The product name is NOT {product_name}, but {text_title}"

    def add_product_to_cart(self, quantity: str, buy_option: BuyOption, size=None):
        if size:
            self.click_element(f'//label[contains(text(), "{size}")]')
            print()
        if quantity.isdigit():
            self.type_to_element(l.product_amount_input_field_shopping_page, quantity)
        else:
            raise Exception("Please use digits for quantity")
        if buy_option == BuyOption.BUY_IT_NOW:
            self.click_element(l.buy_it_now_shopping_page)
        elif buy_option == BuyOption.ADD_TO_CART:
            self.click_element(l.add_to_cart_shopping_page)
            self.click_element(l.continue_shopping_cart_shopping_page)

    def navigate_to_cart(self):
        self.scroll_to_element(l.cart_icon_shopping_page)
        self.click_element(l.cart_icon_shopping_page)
