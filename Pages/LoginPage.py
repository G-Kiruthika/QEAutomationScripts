# LoginPage.py
"""
Page Object Model for Login Page
Implements Selenium Python best practices.
Handles navigation, email/password entry, login, and validation of email length including excessive input handling.
Locators are loaded from Locators.json.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import os

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.locators = self._load_locators()
        self.wait = WebDriverWait(self.driver, 10)

    def _load_locators(self):
        # Load locators from Locators.json
        locators_path = os.path.join(os.path.dirname(__file__), '../Locators.json')
        with open(locators_path, 'r') as f:
            return json.load(f)["LoginPage"]

    def navigate_to_login(self, url=None):
        """
        Navigates to the login page. If URL is provided, uses it; else uses default from locator.
        """
        login_url = url if url else self.locators.get("url")
        self.driver.get(login_url)
        self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, self.locators["inputs"]["emailField"].split('=')[1])
            )
        )

    def enter_email(self, email):
        """
        Enters the provided email in the email field.
        Handles truncation if input exceeds max length.
        """
        email_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, self.locators["inputs"]["emailField"].split('=')[1])
            )
        )
        email_field.clear()
        email_field.send_keys(email)

    def get_email_field_value(self):
        """
        Returns the current value of the email field.
        Useful for checking truncation or value after excessive input.
        """
        email_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, self.locators["inputs"]["emailField"].split('=')[1])
            )
        )
        return email_field.get_attribute("value")

    def enter_password(self, password):
        """
        Enters the provided password in the password field.
        """
        password_field = self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, self.locators["inputs"]["passwordField"].split('=')[1])
            )
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        """
        Clicks the login button.
        """
        login_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, self.locators["buttons"]["loginSubmit"].split('=')[1])
            )
        )
        login_button.click()

    def get_email_length_error(self):
        """
        Returns the error message displayed for excessive email length, if any.
        Returns None if no error is present.
        """
        try:
            error_elem = self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, self.locators["messages"]["validationError"])
                )
            )
            return error_elem.text
        except TimeoutException:
            return None

    def validate_email_max_length(self, input_email):
        """
        Validates system response when entering an email at or exceeding max allowed length.
        Returns a dict with field value and error message (if any).
        """
        self.enter_email(input_email)
        field_value = self.get_email_field_value()
        error_msg = self.get_email_length_error()
        return {
            "entered": input_email,
            "field_value": field_value,
            "error": error_msg
        }

    # --- New methods for TC-LOGIN-014: Handling leading/trailing spaces in email/password ---

    def login_with_spaces(self, email, password):
        """
        Performs login using email and password with leading/trailing spaces.
        Returns a dict with observed outcomes.
        """
        self.navigate_to_login(self.locators["url"])
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

        outcome = {
            "email_entered": email,
            "email_field_value": self.get_email_field_value(),
            "password_entered": password,
            "login_success": False,
            "error_message": None,
            "dashboard_present": False
        }

        # Check for dashboard header (successful login)
        try:
            dashboard_header = self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, self.locators["postLogin"]["dashboardHeader"])
                )
            )
            outcome["login_success"] = True
            outcome["dashboard_present"] = True
        except TimeoutException:
            # Check for error/validation messages
            error_message = None
            try:
                error_elem = self.driver.find_element(
                    By.CSS_SELECTOR, self.locators["messages"]["errorMessage"]
                )
                error_message = error_elem.text
            except Exception:
                # Check for validation error
                try:
                    validation_elem = self.driver.find_element(
                        By.CSS_SELECTOR, self.locators["messages"]["validationError"]
                    )
                    error_message = validation_elem.text
                except Exception:
                    pass
            outcome["error_message"] = error_message

        return outcome

    def is_login_successful(self):
        """
        Checks if login was successful by verifying dashboard header and user profile icon.
        Returns True if both are present, False otherwise.
        """
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, self.locators["postLogin"]["dashboardHeader"])
                )
            )
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, self.locators["postLogin"]["userProfileIcon"])
                )
            )
            return True
        except TimeoutException:
            return False

    def get_login_error_message(self):
        """
        Returns any error or validation message displayed after login attempt.
        Returns None if no message is present.
        """
        try:
            error_elem = self.driver.find_element(
                By.CSS_SELECTOR, self.locators["messages"]["errorMessage"]
            )
            return error_elem.text
        except Exception:
            try:
                validation_elem = self.driver.find_element(
                    By.CSS_SELECTOR, self.locators["messages"]["validationError"]
                )
                return validation_elem.text
            except Exception:
                return None

    # --- End of new methods for TC-LOGIN-014 ---

    # Existing methods preserved below (if any)
    # Add any other legacy methods here as needed
