import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

class LoginPage:
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    LOGIN_BUTTON = (By.ID, "login-submit")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[contains(text(), 'Mandatory fields are required')]")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def navigate_to_login(self):
        self.driver.get(self.URL)
        assert self.driver.current_url.startswith(self.URL), "Login page not displayed"

    def enter_email(self, email: str):
        email_input = self.driver.find_element(*self.EMAIL_FIELD)
        email_input.clear()
        email_input.send_keys(email)
        assert email_input.get_attribute("value") == email, "Email not accepted in the field"

    def leave_password_empty(self):
        password_input = self.driver.find_element(*self.PASSWORD_FIELD)
        password_input.clear()
        assert password_input.get_attribute("value") == "", "Password field is not empty"

    def click_login(self):
        login_btn = self.driver.find_element(*self.LOGIN_BUTTON)
        login_btn.click()
        time.sleep(1)

    def verify_validation_error(self):
        # Check for either validation error or empty field prompt
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
        assert any(["Password field is required" in t or "Please enter your password" in t or "Mandatory fields are required" in t for t in error_texts]), "Validation error not displayed as expected"

    def verify_no_authentication_attempt(self):
        # User should remain on login page, no dashboard/user icon
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
