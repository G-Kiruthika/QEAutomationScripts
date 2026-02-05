# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object Model for the Login Page.
    Implements actions and verifications for TC_LOGIN_001.
    """

    # Locators from Locators.json
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    def navigate_to_login_page(self):
        """
        Navigates to the login page URL.
        """
        self.driver.get(self.URL)
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(self.EMAIL_FIELD)
            )
        except TimeoutException:
            raise Exception("Login screen did not load within timeout.")

    def enter_invalid_credentials(self, username: str, password: str):
        """
        Enters invalid credentials into the login form and submits.
        """
        email_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD)
        )
        password_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD)
        )
        email_input.clear()
        email_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)

        login_button = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON)
        )
        login_button.click()

    def is_error_message_displayed(self, expected_message: str = "Invalid username or password. Please try again.") -> bool:
        """
        Verifies if the error message for invalid credentials is displayed.
        """
        try:
            error_element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            actual_message = error_element.text.strip()
            return actual_message == expected_message
        except (TimeoutException, NoSuchElementException):
            return False
