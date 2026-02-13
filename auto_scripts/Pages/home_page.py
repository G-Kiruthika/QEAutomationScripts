from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    WELCOME_BANNER = (By.CSS_SELECTOR, ".welcome")
    LOGOUT_BUTTON = (By.ID, "logoutBtn")

    def __init__(self, driver):
        super().__init__(driver)

    def click_logout(self):
        self.click_element(self.LOGOUT_BUTTON)

    def navigate_to_profile(self):
        self.click_element(self.WELCOME_BANNER)

    def is_welcome_banner_visible(self):
        return self.is_element_visible(self.WELCOME_BANNER)

    def is_logged_out(self):
        return self.is_element_visible(self.LOGOUT_BUTTON)
