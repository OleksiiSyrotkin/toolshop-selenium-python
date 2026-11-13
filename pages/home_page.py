from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage, dt
from utils.helpers import parse_price


class HomePage(BasePage):
    url = "/"

    CARDS = (By.CSS_SELECTOR, "a.card")
    PRODUCT_NAME = dt("product-name")
    PRODUCT_PRICE = dt("product-price")
    SEARCH_INPUT = dt("search-query")
    SEARCH_SUBMIT = dt("search-submit")
    SEARCH_RESET = dt("search-reset")
    SORT = dt("sort")
    NEXT_PAGE = dt("pagination-next")

    def product_names(self):
        return [el.text.strip() for el in self.find_all(self.PRODUCT_NAME)]

    def product_prices(self):
        return [parse_price(el.text) for el in self.find_all(self.PRODUCT_PRICE)]

    def search(self, term):
        self.type(self.SEARCH_INPUT, term)
        self.click(self.SEARCH_SUBMIT)

    def wait_for_names(self, condition):
        self.wait.until(lambda _: self._safe(lambda: condition(self.product_names())))
        return self.product_names()

    def wait_for_prices(self, condition):
        self.wait.until(lambda _: self._safe(lambda: condition(self.product_prices())))
        return self.product_prices()

    def sort_by(self, value):
        Select(self.find(self.SORT)).select_by_value(value)

    def open_product(self, name):
        for card in self.find_all(self.CARDS):
            if card.find_element(*self.PRODUCT_NAME).text.strip() == name:
                card.click()
                return
        raise AssertionError(f"product '{name}' not found on page")

    @staticmethod
    def _safe(fn):
        try:
            return fn()
        except Exception:
            return False
