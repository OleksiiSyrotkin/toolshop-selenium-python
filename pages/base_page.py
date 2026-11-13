from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


def dt(value):
    return By.CSS_SELECTOR, f'[data-test="{value}"]'


class BasePage:
    url = ""
    base_url = config.BASE_URL

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.TIMEOUT)

    def open(self):
        self.driver.get(self.base_url + self.url)
        return self

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        self.wait.until(EC.visibility_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text.strip()

    def is_visible(self, locator, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def wait_for_url(self, part):
        self.wait.until(EC.url_contains(part))
