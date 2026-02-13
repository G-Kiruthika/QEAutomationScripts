from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    # Locators from metadata (no duplicates, all required)
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'loginBtn')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.error-msg')

    def __init__(self, driver):
        self.driver = driver

    # Actions from metadata
    def enter_username(self, username):
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    # Validations from metadata
    def is_error_message_displayed(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        )

    def get_error_message_text(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text
