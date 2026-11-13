from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage, dt
from utils.helpers import parse_price


class ProductPage(BasePage):
    NAME = dt("product-name")
    PRICE = dt("unit-price")
    QUANTITY = dt("quantity")
    INCREASE = dt("increase-quantity")
    DECREASE = dt("decrease-quantity")
    ADD_TO_CART = dt("add-to-cart")
    CART_BADGE = dt("cart-quantity")
    TOAST = (By.CSS_SELECTOR, "#toast-container")

    def open_by_id(self, product_id):
        self.driver.get(f"{self.base_url}/product/{product_id}")
        self.find(self.NAME)
        return self

    def name(self):
        return self.text_of(self.NAME)

    def price(self):
        return parse_price(self.text_of(self.PRICE))

    def quantity(self):
        return int(self.find(self.QUANTITY).get_attribute("value"))

    def set_quantity(self, qty):
        while self.quantity() < qty:
            self.click(self.INCREASE)
        while self.quantity() > qty:
            self.click(self.DECREASE)

    def add_to_cart(self, qty=1):
        self.set_quantity(qty)
        self.click(self.ADD_TO_CART)
        return self.text_of(self.TOAST)

    def wait_toast_gone(self):
        self.wait.until(EC.invisibility_of_element_located(self.TOAST))

    def cart_count(self):
        return int(self.text_of(self.CART_BADGE))
