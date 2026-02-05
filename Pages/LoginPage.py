# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://example-ecommerce.com/login"

    # Locators
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout)

    def navigate_to_login(self):
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))

    def enter_email(self, email: str):
        email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password: str):
        password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_elem.clear()
        password_elem.send_keys(password)

    def toggle_remember_me(self, check: bool):
        checkbox = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
        if checkbox.is_selected() != check:
            checkbox.click()

    def click_login(self):
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        submit_btn.click()

    def click_forgot_password(self):
        link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
        link.click()

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error_elem.text
        except:
            return None

    def get_validation_error(self):
        try:
            validation_elem = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return validation_elem.text
        except:
            return None

    def is_empty_field_prompt_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
            return True
        except:
            return False

    def is_dashboard_header_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except:
            return False

    def is_user_profile_icon_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except:
            return False

    def login_with_invalid_credentials(self, email: str, password: str):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def verify_invalid_login_error(self):
        error_text = self.get_error_message()
        expected_error = "Invalid username or password. Please try again."
        return error_text == expected_error
