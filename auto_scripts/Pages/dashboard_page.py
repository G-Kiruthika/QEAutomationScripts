from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    WELCOME_BANNER = (By.CSS_SELECTOR, ".welcome-banner")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")

    def __init__(self, driver):
        super().__init__(driver)

    def is_welcome_banner_visible(self):
        return self.is_element_visible(self.WELCOME_BANNER)

    def click_logout_link(self):
        self.click_element(self.LOGOUT_LINK)
