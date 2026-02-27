from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class RegistrationPage:
    EMAIL_INPUT = (By.ID, 'email_input')
    PASSWORD_INPUT = (By.ID, 'password_input')
    NAME_INPUT = (By.ID, 'name_input')
    REGISTER_BUTTON = (By.ID, 'register_button')
    ERROR_MESSAGE = (By.ID, 'error_message')

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def register_user(self, email, password, name):
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.NAME_INPUT).send_keys(name)
        self.driver.find_element(*self.REGISTER_BUTTON).click()

    def submit_registration(self):
        self.driver.find_element(*self.REGISTER_BUTTON).click()

    def validate_registration_success(self):
        # This method should check for successful registration, e.g., by checking for a redirect or success message
        # Placeholder: Replace with actual validation logic
        return 'success' in self.driver.current_url or self.driver.find_elements(By.CLASS_NAME, 'success-message')

    def validate_error_message(self, expected_message=None):
        error_elem = self.driver.find_element(*self.ERROR_MESSAGE)
        if expected_message:
            return error_elem.text == expected_message
        return error_elem.is_displayed()
