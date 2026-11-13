import uuid

import allure
import pytest

import config
from pages.account_page import AccountPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@allure.feature("Login")
class TestLogin:

    @pytest.mark.smoke
    @allure.title("Customer can log in with valid credentials")
    def test_valid_login(self, driver):
        LoginPage(driver).open().login(config.USER_EMAIL, config.USER_PASSWORD)

        account = AccountPage(driver)
        account.wait_for_url("/account")
        assert account.title() == "My account"
        assert account.user_name() == config.USER_FULL_NAME

    @allure.title("Unknown user can't log in")
    def test_unknown_user(self, driver):
        page = LoginPage(driver).open()
        page.login(f"nobody_{uuid.uuid4().hex[:8]}@example.com", "wrong_password_123")

        assert "Invalid email or password" in page.login_error()
        assert "/auth/login" in driver.current_url

    @allure.title("Empty form shows required field errors")
    def test_empty_form(self, driver):
        page = LoginPage(driver).open()
        page.submit_empty()

        assert "required" in page.email_error().lower()
        assert "required" in page.password_error().lower()

    @pytest.mark.parametrize("email", ["not-an-email", "user@", "@mail.com"])
    def test_invalid_email_format(self, driver, email):
        page = LoginPage(driver).open()
        page.login(email, "whatever1")

        assert page.is_visible(page.EMAIL_ERROR)

    def test_logout(self, driver):
        LoginPage(driver).open().login(config.USER_EMAIL, config.USER_PASSWORD)
        account = AccountPage(driver)
        account.wait_for_url("/account")

        account.sign_out()

        assert account.is_visible(account.SIGN_IN)
