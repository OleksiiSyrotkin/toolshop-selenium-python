from pages.base_page import BasePage, dt


class LoginPage(BasePage):
    url = "/auth/login"

    EMAIL = dt("email")
    PASSWORD = dt("password")
    SUBMIT = dt("login-submit")
    LOGIN_ERROR = dt("login-error")
    EMAIL_ERROR = dt("email-error")
    PASSWORD_ERROR = dt("password-error")

    def login(self, email, password):
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def submit_empty(self):
        self.click(self.SUBMIT)

    def login_error(self):
        return self.text_of(self.LOGIN_ERROR)

    def email_error(self):
        return self.text_of(self.EMAIL_ERROR)

    def password_error(self):
        return self.text_of(self.PASSWORD_ERROR)
