from selenium.webdriver.common.by import By
from auto_scripts.Pages.BasePage import BasePage

class HomePage(BasePage):
    WELCOME_BANNER = (By.CSS_SELECTOR, '.welcome-banner')
    LOGOUT_BUTTON = (By.XPATH, "//a[@id='logout'")

    def get_welcome_banner_text(self):
        return self.driver.find_element(*self.WELCOME_BANNER).text

    def click_logout_button(self):
        self.driver.find_element(*self.LOGOUT_BUTTON).click()

    def is_logout_button_visible(self):
        return self.is_element_visible(self.LOGOUT_BUTTON)
