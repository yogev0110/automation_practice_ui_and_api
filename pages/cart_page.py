from pages.base_page import BasePage
from locators import web_locators as l
import re

class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def get_cart_list(self):
        products_elements = self.find_multiple_element(l.cart_item_name)
        product_quantities = self.find_multiple_element(l.cart_item_quantity)
        product_prices = self.find_multiple_element(l.cart_items_price)
        product_sizes = self.find_multiple_element(l.cart_item_size)

        products_in_cart = []
        for _ in range(len(products_elements)):
            product_name = product_price = product_quantity = product_size = None
            if products_elements[_].text is not None:
                product_name = products_elements[_].text
            if product_prices[_] is not None:
                product_price = product_prices[_].text
            if product_quantities is not None:
                product_quantity = product_quantities[_].text
            if product_sizes is not None:
                product_size = product_sizes[_].text
            products_in_cart.append((product_name, product_price, product_size, product_quantity))
        total_price = self.get_text(l.total_price_cart_page).split()[0]
        print()

    def click_on_checkout(self):
        self.scroll_to_element(l.checkout_button_cart_page)
        self.click_element(l.checkout_button_cart_page)

    def get_and_verify_total_price(self, input_total_price_with_unit: str):
        cart_price_ui_with_unit = self.get_text(l.email_field_payment_page)
        assert cart_price_ui_with_unit == input_total_price_with_unit, f'The Total price from the UI is not the same ' \
                                                                       f'as input, UI = {cart_price_ui_with_unit}, ' \
                                                                       f'Input = {input_total_price_with_unit} '
        cart_price_ui = float(re.findall(r'\d+\.\d+', cart_price_ui_with_unit)[0])
        input_total_price = float(re.findall(r'\d+\.\d+', input_total_price_with_unit)[0])
        assert cart_price_ui == input_total_price, f'The Total price from the UI is not the same as input,' \
                                                   f'UI = {cart_price_ui}, Input = {input_total_price}'

