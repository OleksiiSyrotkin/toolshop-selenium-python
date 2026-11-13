from pages.base_page import BasePage, dt
from utils.helpers import parse_price


class CartPage(BasePage):
    url = "/checkout"

    TITLE = dt("product-title")
    QUANTITY = dt("product-quantity")
    PRICE = dt("product-price")
    LINE_PRICE = dt("line-price")
    TOTAL = dt("cart-total")
    PROCEED = dt("proceed-1")

    def items(self):
        titles = self.find_all(self.TITLE)
        qtys = self.driver.find_elements(*self.QUANTITY)
        prices = self.driver.find_elements(*self.PRICE)
        lines = self.driver.find_elements(*self.LINE_PRICE)
        return [
            {
                "name": t.text.strip(),
                "qty": int(q.get_attribute("value")),
                "price": parse_price(p.text),
                "line": parse_price(l.text),
            }
            for t, q, p, l in zip(titles, qtys, prices, lines)
        ]

    def total(self):
        return parse_price(self.text_of(self.TOTAL))
