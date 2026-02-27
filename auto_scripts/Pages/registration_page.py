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

    # --- Missing Locators (per metadata) ---
    EMAIL_INPUT_PLACEHOLDER = (By.ID, 'email_input_placeholder')
    PASSWORD_INPUT_PLACEHOLDER = (By.ID, 'password_input_placeholder')
    NAME_INPUT_PLACEHOLDER = (By.ID, 'name_input_placeholder')
    REGISTER_BUTTON_PLACEHOLDER = (By.ID, 'register_button_placeholder')
    ERROR_MESSAGE_PLACEHOLDER = (By.ID, 'error_message_placeholder')

    # --- Missing Actions (per metadata) ---
    def enter_email(self, email):
        self.driver.find_element(*self.EMAIL_INPUT_PLACEHOLDER).clear()
        self.driver.find_element(*self.EMAIL_INPUT_PLACEHOLDER).send_keys(email)

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT_PLACEHOLDER).clear()
        self.driver.find_element(*self.PASSWORD_INPUT_PLACEHOLDER).send_keys(password)

    def enter_name(self, name):
        self.driver.find_element(*self.NAME_INPUT_PLACEHOLDER).clear()
        self.driver.find_element(*self.NAME_INPUT_PLACEHOLDER).send_keys(name)

    # --- Missing Validations (per metadata) ---
    def validate_registration_page_displayed(self):
        return self.driver.find_element(*self.REGISTER_BUTTON_PLACEHOLDER).is_displayed()

    def validate_fields_accept_input(self):
        try:
            self.driver.find_element(*self.EMAIL_INPUT_PLACEHOLDER).send_keys('test@example.com')
            self.driver.find_element(*self.PASSWORD_INPUT_PLACEHOLDER).send_keys('password123')
            self.driver.find_element(*self.NAME_INPUT_PLACEHOLDER).send_keys('Test User')
            return True
        except Exception:
            return False