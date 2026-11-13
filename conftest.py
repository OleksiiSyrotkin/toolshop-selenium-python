import os

import allure
import pytest
from selenium import webdriver

from api.toolshop_client import ToolshopClient


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", choices=["chrome", "firefox"])
    parser.addoption("--headless", action="store_true", default=bool(os.getenv("CI")))


def _make_driver(name, headless):
    if name == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1920, 1080)
        return driver

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("prefs", {"credentials_enable_service": False})
    return webdriver.Chrome(options=options)


@pytest.fixture
def driver(request):
    drv = _make_driver(request.config.getoption("--browser"), request.config.getoption("--headless"))
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def api():
    return ToolshopClient()


@pytest.fixture(scope="session")
def token(api):
    return api.login_as_customer()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    drv = item.funcargs.get("driver")
    if drv is None:
        return
    allure.attach(drv.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
    allure.attach(drv.current_url, name="url", attachment_type=allure.attachment_type.TEXT)
