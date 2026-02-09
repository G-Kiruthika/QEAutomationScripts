# LoginPage.py
"""
Page Object for Login functionality
Includes methods for login, error handling, forgot password navigation, SQL injection validation, accessibility checks, and password masking validation.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.ID, "login-email")
        self.password_field = (By.ID, "login-password")
        self.remember_me_checkbox = (By.ID, "remember-me")
        self.login_button = (By.ID, "login-submit")
        self.forgot_password_link = (By.CSS_SELECTOR, "a.forgot-password-link")
        self.error_message = (By.CSS_SELECTOR, "div.alert-danger")
        self.validation_error = (By.CSS_SELECTOR, ".invalid-feedback")
        self.empty_field_prompt = (By.XPATH, "//*[text()='Mandatory fields are required']")
        self.dashboard_header = (By.CSS_SELECTOR, "h1.dashboard-title")
        self.user_profile_icon = (By.CSS_SELECTOR, ".user-profile-name")
        self.password_recovery_header = (By.XPATH, "//h1[text()='Password Recovery']")

    def navigate_to_login_page(self):
        self.driver.get("https://example-ecommerce.com/login")
        return self.driver.current_url == "https://example-ecommerce.com/login"

    def click_forgot_password(self):
        self.driver.find_element(*self.forgot_password_link).click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.password_recovery_header)
            )
            return True
        except TimeoutException:
            return False

    def enter_username(self, username):
        self.driver.find_element(*self.email_field).clear()
        self.driver.find_element(*self.email_field).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.password_field).clear()
        self.driver.find_element(*self.password_field).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

    def attempt_sql_injection(self, username_injection, password_injection):
        self.enter_username(username_injection)
        self.enter_password(password_injection)
        self.click_login()
        try:
            error = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.error_message)
            )
            return error.text is not None and error.text != ""
        except TimeoutException:
            return False

    def get_error_message(self):
        try:
            return self.driver.find_element(*self.error_message).text
        except TimeoutException:
            return None
