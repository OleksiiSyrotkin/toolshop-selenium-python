import allure
import pytest

from pages.home_page import HomePage

pytestmark = pytest.mark.ui


@allure.feature("Catalog")
class TestSearch:

    @pytest.mark.smoke
    @pytest.mark.parametrize("term", ["pliers", "hammer"])
    def test_search_returns_matching_products(self, driver, term):
        page = HomePage(driver).open()
        page.search(term)

        names = page.wait_for_names(lambda items: items and all(term in n.lower() for n in items))
        assert names

    def test_search_results_match_api(self, driver, api):
        expected = sorted(p["name"] for p in api.search("pliers").json()["data"])

        page = HomePage(driver).open()
        page.search("pliers")
        actual = page.wait_for_names(lambda items: sorted(items) == expected)

        assert sorted(actual) == expected


@allure.feature("Catalog")
class TestSorting:

    @pytest.mark.parametrize("option, reverse", [("price,asc", False), ("price,desc", True)])
    def test_sort_by_price(self, driver, option, reverse):
        page = HomePage(driver).open()
        page.sort_by(option)

        prices = page.wait_for_prices(lambda p: p == sorted(p, reverse=reverse))
        assert prices == sorted(prices, reverse=reverse)

    @pytest.mark.parametrize("option, reverse", [("name,asc", False), ("name,desc", True)])
    def test_sort_by_name(self, driver, option, reverse):
        page = HomePage(driver).open()
        page.sort_by(option)

        names = page.wait_for_names(lambda n: n == sorted(n, key=str.lower, reverse=reverse))
        assert names == sorted(names, key=str.lower, reverse=reverse)
