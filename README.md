# toolshop-selenium-python

[![tests](https://github.com/OleksiiSyrotkin/toolshop-selenium-python/actions/workflows/tests.yml/badge.svg)](https://github.com/OleksiiSyrotkin/toolshop-selenium-python/actions/workflows/tests.yml)

UI and API tests for [Practice Software Testing (Toolshop)](https://practicesoftwaretesting.com) - a demo e-commerce app for tools. Python + Selenium + pytest.

Allure report from the latest run on `main`: https://oleksiisyrotkin.github.io/toolshop-selenium-python/

## What is tested

| Area | Checks |
|---|---|
| Login | valid login, unknown user, empty form validation, email format validation, logout |
| Catalog | search (UI results compared with API), sorting by price and name |
| Product page | name and price on the page match API data, opening a product from the catalog |
| Cart | add with quantity, toast message, cart badge, line prices and cart total |
| API | products list and pagination, product by id, 404, search, sorting, categories, login, `/users/me`, auth errors, JSON schema validation |

## Stack

- Python 3.12
- Selenium 4 (drivers are downloaded automatically by Selenium Manager)
- pytest, pytest-xdist (parallel run), pytest-rerunfailures
- requests + jsonschema for API tests
- Allure for reporting
- GitHub Actions: API tests on every push, Allure report published to GitHub Pages

## Project structure

```
api/
  toolshop_client.py     thin wrapper over requests for Toolshop API
pages/
  base_page.py           common actions with explicit waits, dt() helper for data-test locators
  login_page.py
  account_page.py
  home_page.py           catalog: search, sorting, product cards
  product_page.py
  cart_page.py
tests/
  api/                   API tests and JSON schemas
  ui/                    UI tests
utils/helpers.py         price parsing
config.py                urls and test user (can be overridden from .env)
conftest.py              driver fixture, CLI options, screenshot on failure
```

## Approach

- **Page Object Model.** Tests don't contain locators or Selenium calls, only page methods and asserts.
- **Locators.** Toolshop has `data-test` attributes on most elements, so almost all locators are `[data-test="..."]`. They don't depend on layout and CSS classes.
- **Waits.** Only explicit waits (`WebDriverWait`), no `time.sleep`. For search and sorting the test waits until the list on the page satisfies the condition (for example "all prices are sorted ascending"). Otherwise the check could run on the old list before Angular re-renders it.
- **API + UI together.** Some UI tests take expected data from the API (product price, search results). This way the tests don't break when the demo data changes, and they also check that the frontend shows what the backend returns.
- **Test data.** Negative login tests use a random non-existing email, so the shared demo account doesn't get locked after several failed attempts.
- **Each test gets a fresh browser**, so the cart and session don't leak between tests and the tests can run in parallel.
- **On failure** a screenshot and the current URL are attached to the Allure report.

## How to run

Requirements: Python 3.10+, Chrome or Firefox.

```bash
git clone https://github.com/OleksiiSyrotkin/toolshop-selenium-python.git
cd toolshop-selenium-python

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

```bash
pytest                                  # everything
pytest -m api                           # API only, no browser
pytest -m ui                            # UI only
pytest -m smoke                         # critical checks
pytest tests/ui/test_cart.py            # one file

pytest -m ui --browser=firefox          # Firefox instead of Chrome
pytest -m ui --headless                 # without browser window
pytest -m ui -n 4                       # 4 parallel workers
```

In CI (`CI` env variable is set) the browser runs headless automatically.

Allure report locally (needs [Allure CLI](https://allurereport.org/docs/install/)):

```bash
allure serve allure-results
```

## Configuration

Default values are in `config.py`. To override, copy `.env.example` to `.env`:

```
BASE_URL=https://practicesoftwaretesting.com
API_URL=https://api.practicesoftwaretesting.com
USER_EMAIL=customer@practicesoftwaretesting.com
USER_PASSWORD=welcome01
```

These are public demo credentials from the Toolshop site.

## CI

`.github/workflows/tests.yml`:

1. `api` - API tests
2. `report` - builds the Allure report and publishes it to GitHub Pages

UI tests are not run in CI: practicesoftwaretesting.com shows a Cloudflare "Verify you are human" page to GitHub Actions runners, so the browser never gets to the app. UI tests are run locally (`pytest -m ui`).

Runs on push to `main`, on pull requests, manually and every Monday (to notice when the demo site changes).

## Notes

- Toolshop is a public demo app, sometimes it's slow or down. If UI tests are flaky locally, run them with `--reruns 1`.
- Demo data is reset from time to time, so tests don't rely on hardcoded product ids.
