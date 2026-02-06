import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
import pickle

class LoginPage:
    """
    PageClass for LoginPage interactions and validations.
    Covers navigation, field entry, login, remember-me, session persistence, and validation/error checks for test automation.
    """
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[contains(text(), 'Mandatory fields are required')]")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")  # Assumed locator

    def __init__(self, driver: WebDriver):
        """
        Initialize with Selenium WebDriver instance.
        """
        self.driver = driver

    def navigate_to_login(self):
        """
        Navigate to login page and verify display.
        """
        self.driver.get(self.URL)
        assert self.driver.current_url.startswith(self.URL), "Login page not displayed"

    def leave_email_empty(self):
        """
        Clear the email field and verify it is empty.
        """
        email_input = self.driver.find_element(*self.EMAIL_FIELD)
        email_input.clear()
        assert email_input.get_attribute("value") == "", "Email field is not empty"

    def enter_email(self, email: str):
        """
        Enter email in the field and verify value.
        """
        email_input = self.driver.find_element(*self.EMAIL_FIELD)
        email_input.clear()
        email_input.send_keys(email)
        assert email_input.get_attribute("value") == email, "Email not accepted in the field"

    def leave_password_empty(self):
        """
        Clear the password field and verify it is empty.
        """
        password_input = self.driver.find_element(*self.PASSWORD_FIELD)
        password_input.clear()
        assert password_input.get_attribute("value") == "", "Password field is not empty"

    def enter_password(self, password: str):
        """
        Enter password in the field and verify value.
        """
        password_input = self.driver.find_element(*self.PASSWORD_FIELD)
        password_input.clear()
        password_input.send_keys(password)
        assert password_input.get_attribute("value") == password, "Password not accepted in the field"

    def click_login(self):
        """
        Click the login button to submit credentials.
        """
        login_btn = self.driver.find_element(*self.LOGIN_BUTTON)
        login_btn.click()
        time.sleep(1)

    def verify_validation_error(self):
        """
        Verify that validation errors are displayed for empty fields.
        """
        error_texts = []
        try:
            error_elem = self.driver.find_element(*self.VALIDATION_ERROR)
            error_texts.append(error_elem.text)
        except NoSuchElementException:
            pass
        try:
            prompt_elem = self.driver.find_element(*self.EMPTY_FIELD_PROMPT)
            error_texts.append(prompt_elem.text)
        except NoSuchElementException:
            pass
        assert any([
            "Email and password are required" in t or
            "Password field is required" in t or
            "Please enter your password" in t or
            "Mandatory fields are required" in t for t in error_texts
        ]), "Validation error not displayed as expected"

    def verify_no_authentication_attempt(self):
        """
        Verify user remains on login page and authentication is not processed.
        """
        current_url = self.driver.current_url
        assert current_url.startswith(self.URL), "User navigated away from login page, authentication may have been processed"
        try:
            dashboard_header = self.driver.find_element(By.CSS_SELECTOR, "h1.dashboard-title")
            assert False, "Dashboard header found, authentication should not have been processed"
        except NoSuchElementException:
            pass
        try:
            user_icon = self.driver.find_element(By.CSS_SELECTOR, ".user-profile-name")
            assert False, "User profile icon found, authentication should not have been processed"
        except NoSuchElementException:
            pass

    # --- New Functions for TC-LOGIN-007 ---

    def check_remember_me(self):
        """
        Check the 'Remember Me' checkbox if not already checked.
        """
        checkbox = self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
        if not checkbox.is_selected():
            checkbox.click()
        assert checkbox.is_selected(), "Remember Me checkbox is not checked!"

    def save_cookies(self, filepath: str = "cookies.pkl"):
        """
        Save cookies after login for session persistence.
        """
        with open(filepath, "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)

    def load_cookies(self, filepath: str = "cookies.pkl"):
        """
        Load cookies to restore session.
        """
        with open(filepath, "rb") as file:
            cookies = pickle.load(file)
        self.driver.get(self.URL)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

    def is_logged_in(self):
        """
        Verify automatic login/session persistence by checking dashboard presence.
        """
        try:
            dashboard_header = self.driver.find_element(By.CSS_SELECTOR, "h1.dashboard-title")
            return dashboard_header.is_displayed()
        except NoSuchElementException:
            return False
