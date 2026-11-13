from pages.base_page import BasePage, dt


class AccountPage(BasePage):
    url = "/account"

    TITLE = dt("page-title")
    USER_MENU = dt("nav-menu")
    SIGN_OUT = dt("nav-sign-out")
    SIGN_IN = dt("nav-sign-in")

    def title(self):
        return self.text_of(self.TITLE)

    def user_name(self):
        return self.text_of(self.USER_MENU)

    def sign_out(self):
        self.click(self.USER_MENU)
        self.click(self.SIGN_OUT)
        self.find(self.SIGN_IN)
