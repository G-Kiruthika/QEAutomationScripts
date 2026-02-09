# LoginPage.py
"""
Page Object Model for the Login Page (Selenium version)
Author: QE Automation Orchestration Agent
Description: This class encapsulates interactions with the Login Page, including methods for login, error validation, 'Remember Me', and session persistence checks. Updated for TC_LOGIN_005 and TC_LOGIN_006.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    URL = "https://example-ecommerce.com/login"

    # Locators from Locators.json
    EMAIL_INPUT = (By.ID, "login-email")
    PASSWORD_INPUT = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_BUTTON = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize LoginPage with WebDriver and timeout.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        """
        Navigate to the login page and wait for email input visibility.
        """
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))

    def enter_email(self, email: str):
        """
        Enter email into the email input field.
        """
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_field.clear()
        email_field.send_keys(email)

    def enter_password(self, password: str):
        """
        Enter password into the password input field.
        """
        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_field.clear()
        password_field.send_keys(password)

    def check_remember_me(self, check: bool = True):
        """
        Check or uncheck the 'Remember Me' checkbox.
        :param check: If True, ensure checkbox is checked; if False, unchecked.
        """
        checkbox = self.wait.until(EC.visibility_of_element_located(self.REMEMBER_ME_CHECKBOX))
        if checkbox.is_selected() != check:
            checkbox.click()

    def click_login(self):
        """
        Click the login button.
        """
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_button.click()

    def is_dashboard_displayed(self):
        """
        Verify if dashboard header is displayed (successful login).
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except TimeoutException:
            return False

    def is_error_message_displayed(self, expected_message: str = None):
        """
        Check if an error message is displayed, optionally matching expected text.
        """
        try:
            error_element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            if expected_message:
                return expected_message in error_element.text
            return True
        except TimeoutException:
            return False

    def is_login_page_displayed(self):
        """
        Verify login page elements are present.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
            self.wait.until(EC.visibility_of_element_located(self.LOGIN_BUTTON))
            return True
        except TimeoutException:
            return False

    def get_validation_error(self):
        """
        Retrieve validation error text from invalid feedback.
        """
        try:
            validation_error = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return validation_error.text
        except TimeoutException:
            return None

    def get_empty_field_prompt(self):
        """
        Retrieve prompt text for empty mandatory fields.
        """
        try:
            prompt = self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
            return prompt.text
        except TimeoutException:
            return None

    def is_user_profile_icon_displayed(self):
        """
        Verify if user profile icon is displayed (post-login).
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except TimeoutException:
            return False

    def verify_session_persistence(self):
        """
        Verify session persistence by checking dashboard or profile icon after reopening browser.
        Should be used after login with 'Remember Me'.
        """
        # Example implementation: assumes driver is re-instantiated with preserved cookies/session
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except TimeoutException:
            return False
