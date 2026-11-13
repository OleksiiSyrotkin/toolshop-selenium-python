import pytest
from jsonschema import validate

from tests.api import schemas

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_products_list(api):
    resp = api.get_products()

    assert resp.status_code == 200
    body = resp.json()
    validate(body, schemas.PRODUCT_PAGE)
    assert body["current_page"] == 1
    assert 0 < len(body["data"]) <= body["per_page"]


def test_pagination_returns_different_products(api):
    first = {p["id"] for p in api.get_products(page=1).json()["data"]}
    second = {p["id"] for p in api.get_products(page=2).json()["data"]}

    assert second
    assert first.isdisjoint(second)


def test_page_out_of_range_is_empty(api):
    last = api.get_products().json()["last_page"]
    body = api.get_products(page=last + 1).json()

    assert body["data"] == []


def test_get_product_by_id(api):
    expected = api.get_products().json()["data"][0]

    resp = api.get_product(expected["id"])

    assert resp.status_code == 200
    validate(resp.json(), schemas.PRODUCT)
    assert resp.json()["name"] == expected["name"]
    assert resp.json()["price"] == expected["price"]


def test_unknown_product_returns_404(api):
    assert api.get_product("does-not-exist").status_code == 404


@pytest.mark.parametrize("term", ["pliers", "hammer", "PLIERS"])
def test_search(api, term):
    resp = api.search(term)

    assert resp.status_code == 200
    names = [p["name"].lower() for p in resp.json()["data"]]
    assert names
    assert all(term.lower() in n for n in names)


def test_search_nothing_found(api):
    assert api.search("qwertyzxcv").json()["data"] == []


def test_sort_by_price(api):
    prices = [p["price"] for p in api.get_products(sort="price,asc").json()["data"]]
    assert prices == sorted(prices)


def test_categories_tree(api):
    resp = api.get_categories()

    assert resp.status_code == 200
    names = [c["name"] for c in resp.json()]
    assert {"Hand Tools", "Power Tools"} <= set(names)
