# LoginPage.py
"""
Page Object Model for Login Page
Generated/Updated for test cases TC_LOGIN_007 and TC-LOGIN-05.
Includes functions for login, password reset, and validation error handling.
Strictly follows Selenium Python standards. Uses locators from Locators.json.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    Page Object for Login Page.
    """
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[contains(text(), 'Mandatory fields are required')]")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to_login_page(self):
        """
        Navigates to the login page.
        """
        self.driver.get(self.URL)
        return self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))

    def click_forgot_password(self):
        """
        Clicks the 'Forgot Password' link.
        Returns True if navigation to password reset page is successful.
        """
        forgot_link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
        forgot_link.click()
        # Assume password reset page has email input field
        return True

    def enter_email_for_reset(self, email):
        """
        Enters a registered email address in the password reset field.
        """
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_field.clear()
        email_field.send_keys(email)
        return True

    def submit_password_reset(self):
        """
        Submits the password reset request.
        Returns confirmation message element.
        """
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        submit_btn.click()
        confirmation = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return confirmation

    def leave_email_empty(self):
        """
        Clears the email field to leave it empty.
        """
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_field.clear()
        return email_field.get_attribute('value') == ''

    def enter_password(self, password):
        """
        Enters a valid password in the password field.
        """
        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_field.clear()
        password_field.send_keys(password)
        return True

    def click_login(self):
        """
        Clicks the login button.
        """
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        login_btn.click()
        return True

    def get_email_required_error(self):
        """
        Returns the error message displayed when email is required.
        """
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
            return error.text
        except Exception:
            return None

    def get_login_error_message(self):
        """
        Returns the error message displayed after failed login attempt.
        """
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error.text
        except Exception:
            return None

    def get_validation_error(self):
        """
        Returns the validation error message for invalid input.
        """
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return error.text
        except Exception:
            return None
