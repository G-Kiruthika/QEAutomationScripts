import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    """
    PageClass for LoginPage interactions and validations.
    Covers navigation, field entry (incl. special characters), login, and authentication result verification for test automation.
    """
    DEFAULT_URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[contains(text(), 'Mandatory fields are required')]")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver, url: str = None):
        """
        Initialize with Selenium WebDriver instance and optional login URL.
        """
        self.driver = driver
        self.url = url if url else self.DEFAULT_URL

    def navigate_to_login(self):
        """
        Navigate to login page and verify display.
        """
        self.driver.get(self.url)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.EMAIL_FIELD)
            )
        except TimeoutException:
            raise AssertionError("Login page is not loaded or email field not found.")
        assert self.driver.current_url.startswith(self.url), "Login page URL mismatch."

    def enter_email(self, email: str):
        """
        Enter email (including special characters) in the field and verify value.
        """
        email_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD)
        )
        email_input.clear()
        email_input.send_keys(email)
        actual_value = email_input.get_attribute("value")
        assert actual_value == email, f"Email not accepted in the field. Expected: {email}, Actual: {actual_value}"

    def enter_password(self, password: str):
        """
        Enter password (including special characters) in the field and verify value.
        """
        password_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD)
        )
        password_input.clear()
        password_input.send_keys(password)
        actual_value = password_input.get_attribute("value")
        assert actual_value == password, f"Password not accepted in the field. Expected: {password}, Actual: {actual_value}"

    def click_login(self):
        """
        Click the login button to submit credentials.
        """
        login_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        login_btn.click()

    def verify_authentication_result(self, expect_success: bool):
        """
        Verify authentication result after login attempt.
        If expect_success is True, checks for dashboard and user profile icon.
        If expect_success is False, checks for error message or validation feedback.
        """
        if expect_success:
            try:
                dashboard_header = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(self.DASHBOARD_HEADER)
                )
                user_icon = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(self.USER_PROFILE_ICON)
                )
                assert dashboard_header.is_displayed(), "Dashboard header not displayed after login."
                assert user_icon.is_displayed(), "User profile icon not displayed after login."
            except TimeoutException:
                raise AssertionError("Login was expected to succeed, but dashboard/user icon not found.")
        else:
            error_displayed = False
            try:
                error_elem = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(self.ERROR_MESSAGE)
                )
                error_displayed = error_elem.is_displayed()
            except TimeoutException:
                pass
            try:
                validation_elem = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(self.VALIDATION_ERROR)
                )
                error_displayed = error_displayed or validation_elem.is_displayed()
            except TimeoutException:
                pass
            assert error_displayed, "Login was expected to fail, but no error or validation message found."

    def is_login_page_displayed(self):
        """
        Returns True if login page is loaded and email/password fields are present.
        """
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.EMAIL_FIELD)
            )
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.PASSWORD_FIELD)
            )
            return True
        except TimeoutException:
            return False
