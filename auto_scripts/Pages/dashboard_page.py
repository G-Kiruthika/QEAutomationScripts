from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    WELCOME_MESSAGE = (By.CSS_SELECTOR, '.welcome')
    LOGOUT_BUTTON = (By.ID, 'logout')

    def click_logout(self):
        self.driver.find_element(*self.LOGOUT_BUTTON).click()

    def is_dashboard_loaded(self):
        return len(self.driver.find_elements(*self.WELCOME_MESSAGE)) > 0
