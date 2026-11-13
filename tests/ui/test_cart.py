import allure
import pytest

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_page import ProductPage

pytestmark = pytest.mark.ui


@allure.feature("Product page")
def test_product_details_match_api(driver, api):
    product = api.find_product_by_name("Combination Pliers")

    page = ProductPage(driver).open_by_id(product["id"])

    assert page.name() == product["name"]
    assert page.price() == product["price"]


@allure.feature("Product page")
def test_open_product_from_catalog(driver):
    home = HomePage(driver).open()
    home.open_product("Combination Pliers")

    page = ProductPage(driver)
    page.wait_for_url("/product/")
    assert page.name() == "Combination Pliers"


@allure.feature("Cart")
class TestCart:

    @pytest.mark.smoke
    def test_add_to_cart(self, driver, api):
        product = api.find_product_by_name("Combination Pliers")
        page = ProductPage(driver).open_by_id(product["id"])

        toast = page.add_to_cart(qty=3)

        assert toast == "Product added to shopping cart."
        assert page.cart_count() == 3

    def test_cart_total(self, driver, api):
        first = api.find_product_by_name("Combination Pliers")
        second = api.find_product_by_name("Slip Joint Pliers")

        page = ProductPage(driver).open_by_id(first["id"])
        page.add_to_cart(qty=2)
        page.wait_toast_gone()
        page.open_by_id(second["id"])
        page.add_to_cart(qty=1)
        page.wait_toast_gone()

        cart = CartPage(driver).open()
        items = cart.items()

        assert {i["name"] for i in items} == {first["name"], second["name"]}
        for item in items:
            assert item["line"] == pytest.approx(item["price"] * item["qty"])
        assert cart.total() == pytest.approx(first["price"] * 2 + second["price"])

    def test_out_of_stock_product_cannot_be_added(self, driver, api):
        product = api.find_product_by_name("Long Nose Pliers")
        assert not product["in_stock"]

        page = ProductPage(driver).open_by_id(product["id"])

        assert page.text_of(page.OUT_OF_STOCK) == "Out of stock"
        assert not page.can_add_to_cart()
        assert not page.can_change_quantity()
