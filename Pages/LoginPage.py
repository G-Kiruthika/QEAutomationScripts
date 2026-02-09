from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://example-ecommerce.com/login"
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

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))

    def enter_email(self, email: str):
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password: str):
        password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_input.clear()
        password_input.send_keys(password)

    def click_remember_me(self):
        checkbox = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_CHECKBOX))
        checkbox.click()

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        login_btn.click()

    def click_forgot_password(self):
        link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK))
        link.click()

    def get_error_message(self):
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return error.text
        except Exception:
            return None

    def get_validation_error(self):
        try:
            error = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return error.text
        except Exception:
            return None

    def is_empty_field_prompt_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
            return True
        except Exception:
            return False

    def is_dashboard_header_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except Exception:
            return False

    def is_user_profile_icon_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except Exception:
            return False
