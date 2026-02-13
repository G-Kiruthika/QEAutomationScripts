from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")

    def enter_username(self, username):
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def is_login_successful(self):
        # Example: Check for presence of dashboard element or successful redirect
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".welcome")
            return True
        except Exception:
            return False

    def is_error_displayed(self):
        # Example: Check for error message element
        return len(self.driver.find_elements(By.CSS_SELECTOR, ".error")) > 0
