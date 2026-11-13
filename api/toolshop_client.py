import requests

import config


class ToolshopClient:
    def __init__(self, base_url=config.API_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _get(self, path, **kwargs):
        return self.session.get(f"{self.base_url}{path}", timeout=15, **kwargs)

    def _post(self, path, **kwargs):
        return self.session.post(f"{self.base_url}{path}", timeout=15, **kwargs)

    def get_products(self, page=1, **params):
        return self._get("/products", params={"page": page, **params})

    def get_product(self, product_id):
        return self._get(f"/products/{product_id}")

    def search(self, query):
        return self._get("/products/search", params={"q": query})

    def get_categories(self):
        return self._get("/categories/tree")

    def get_brands(self):
        return self._get("/brands")

    def login(self, email, password):
        return self._post("/users/login", json={"email": email, "password": password})

    def login_as_customer(self):
        resp = self.login(config.USER_EMAIL, config.USER_PASSWORD)
        resp.raise_for_status()
        return resp.json()["access_token"]

    def me(self, token):
        return self._get("/users/me", headers={"Authorization": f"Bearer {token}"})

    def find_product_by_name(self, name):
        products = self.search(name).json()["data"]
        return next(p for p in products if p["name"] == name)
