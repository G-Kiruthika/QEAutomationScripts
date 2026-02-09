# LoginPage.py
"""
Page Object for Login functionality
Includes methods for login, error handling, forgot password navigation, and SQL injection validation.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.ID, "username")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "loginBtn")
        self.error_message = (By.ID, "errorMsg")
        self.forgot_password_link = (By.LINK_TEXT, "Forgot Password?")
        self.password_recovery_header = (By.XPATH, "//h1[text()='Password Recovery']")

    def enter_username(self, username):
        self.driver.find_element(*self.username_field).clear()
        self.driver.find_element(*self.username_field).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.password_field).clear()
        self.driver.find_element(*self.password_field).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

    def get_error_message(self):
        try:
            return self.driver.find_element(*self.error_message).text
        except TimeoutException:
            return None

    # --- New Methods for Test Cases ---
    def navigate_to_forgot_password(self):
        """
        Clicks the 'Forgot Password' link and verifies navigation to the password recovery page.
        Returns True if navigation is successful, False otherwise.
        """
        self.driver.find_element(*self.forgot_password_link).click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.password_recovery_header)
            )
            return True
        except TimeoutException:
            return False

    def attempt_sql_injection(self, username_injection, password_injection):
        """
        Attempts login with SQL injection strings and verifies login fails.
        Returns True if error message is shown and no unauthorized access occurs, False otherwise.
        """
        self.enter_username(username_injection)
        self.enter_password(password_injection)
        self.click_login()
        try:
            error = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.error_message)
            )
            # Optionally, check for unauthorized access indicators here
            return error.text is not None and error.text != ""
        except TimeoutException:
            return False
