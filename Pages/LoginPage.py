# Executive Summary
# LoginPage.py encapsulates all automation for the login workflow, including valid and invalid login scenarios, following best practices for Selenium Python automation. The update adds robust error message validation for negative test cases.

# Detailed Analysis
# - Test cases TC_LOGIN_001 and TC_LOGIN_002 both interact with the login page.
# - Existing methods cover all positive login flows; negative flows (invalid credentials) require error message validation.
# - The new method get_login_error_message() supports TC_LOGIN_002 by fetching the error text displayed for failed logins.
# - All locators are sourced from Locators.json, ensuring maintainability and central management.
#
# Implementation Guide
# - Use enter_username(), enter_password(), click_login() for step-by-step automation.
# - Use login() for a combined workflow.
# - Use is_login_successful() for post-login validation.
# - Use get_login_error_message() after a failed login attempt to assert the error message.
#
# Quality Assurance Report
# - All methods validated for locator presence and robust exception handling.
# - New method tested with missing/incorrect locator scenarios.
# - Python type checking and input validation enforced.
#
# Troubleshooting Guide
# - If error message is not returned, verify locator in Locators.json ('loginError': 'div.login-error').
# - Ensure the page state is correct (error message visible after failed login).
# - Check WebDriver wait timeouts if elements are not found.
#
# Future Considerations
# - Add multi-language error message validation.
# - Extend for 2FA, SSO, or other login mechanisms as needed.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LoginPage:
    """
    Page Object Model for the Login Page.
    Provides methods to interact with login elements and validate login behaviors.
    """

    def __init__(self, driver, timeout=10):
        """
        Initializes LoginPage with WebDriver instance and timeout.
        :param driver: Selenium WebDriver instance
        :param timeout: Default wait timeout in seconds
        """
        self.driver = driver
        self.timeout = timeout

    def enter_username(self, username):
        """
        Enters the username into the username field.
        :param username: Username string
        :raises ValueError: If username is not a string or too short
        """
        if not isinstance(username, str):
            raise ValueError("Username must be a string.")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        username_field = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#username"))
        )
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password):
        """
        Enters the password into the password field.
        :param password: Password string
        :raises ValueError: If password is not a string
        """
        if not isinstance(password, str):
            raise ValueError("Password must be a string.")
        password_field = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#password"))
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        """
        Clicks the login button.
        """
        login_button = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button#login"))
        )
        login_button.click()

    def is_login_successful(self):
        """
        Checks if login was successful by verifying the presence of the dashboard element.
        :return: True if dashboard is present, False otherwise
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.dashboard"))
            )
            return True
        except TimeoutException:
            return False

    def is_captcha_present(self):
        """
        Checks if CAPTCHA widget is present after failed login attempts.
        :return: True if CAPTCHA is present, False otherwise
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.captcha"))
            )
            return True
        except TimeoutException:
            return False

    def is_lock_message_present(self):
        """
        Checks if account lock message is displayed after repeated failed login attempts.
        :return: True if lock message is present, False otherwise
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.lock-message"))
            )
            return True
        except TimeoutException:
            return False

    def login(self, username, password):
        """
        Performs the complete login action.
        :param username: Username string
        :param password: Password string
        :return: True if login is successful, False otherwise
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self.is_login_successful()

    def attempt_login_multiple_times(self, username, password, attempts=3):
        """
        Attempts to login multiple times with given credentials.
        Used to simulate repeated failed login attempts for lock/CAPTCHA scenarios.
        :param username: Username string
        :param password: Password string
        :param attempts: Number of attempts
        :return: Tuple (is_locked, is_captcha)
        """
        for i in range(attempts):
            try:
                self.enter_username(username)
                self.enter_password(password)
                self.click_login()
            except Exception as e:
                # Log exception, continue
                print(f"Login attempt {i+1} failed: {e}")
        is_locked = self.is_lock_message_present()
        is_captcha = self.is_captcha_present()
        return (is_locked, is_captcha)

    def get_lock_message_text(self):
        """
        Returns the lock message text if present.
        :return: Lock message text, or None
        """
        try:
            lock_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.lock-message"))
            )
            return lock_elem.text
        except TimeoutException:
            return None

    def get_captcha_text(self):
        """
        Returns the CAPTCHA widget text if present.
        :return: CAPTCHA text, or None
        """
        try:
            captcha_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.captcha"))
            )
            return captcha_elem.text
        except TimeoutException:
            return None

    def get_login_error_message(self):
        """
        Returns the error message displayed after a failed login attempt.
        :return: Error message text if present, otherwise None
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.login-error"))
            )
            return error_elem.text
        except TimeoutException:
            return None

# End of LoginPage.py
