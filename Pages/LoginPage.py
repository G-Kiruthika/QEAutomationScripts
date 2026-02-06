# LoginPage.py
"""
Page Object Model for the Login Page
Author: Automation Team
Description: This class encapsulates the interactions and verifications for the Login Page, using locators defined in Locators.json. It includes methods to navigate to the login screen, enter credentials, submit login, and verify error messages as required by TC_LOGIN_001.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object for the Login Screen
    """

    # Locators (from Locators.json)
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initializes the LoginPage with a Selenium WebDriver instance.
        :param driver: Selenium WebDriver
        :param timeout: Default wait timeout for elements
        """
        self.driver = driver
        self.timeout = timeout

    def go_to_login_page(self):
        """
        Navigates the browser to the login page URL and waits for the login form to be visible.
        """
        self.driver.get(self.URL)
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Login email field not visible after navigating to login page."
        )

    def enter_credentials(self, username: str, password: str):
        """
        Enters the username and password into the login form fields.
        :param username: The username/email to enter
        :param password: The password to enter
        """
        email_input = self.driver.find_element(*self.EMAIL_FIELD)
        password_input = self.driver.find_element(*self.PASSWORD_FIELD)
        email_input.clear()
        email_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)

    def submit_login(self):
        """
        Clicks the login submit button to attempt login.
        """
        self.driver.find_element(*self.LOGIN_SUBMIT).click()

    def get_error_message(self) -> str:
        """
        Retrieves the error message displayed after a failed login attempt.
        :return: The error message text
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE),
                message="Error message not visible after invalid login."
            )
            return error_elem.text
        except NoSuchElementException:
            return ""

    # Additional utility methods can be implemented here as needed.
