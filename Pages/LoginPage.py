# LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://example-ecommerce.com/login"

    # Locators from Locators.json
    EMAIL_INPUT = (By.ID, "login-email")
    PASSWORD_INPUT = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_BUTTON = (By.ID, "login-submit")
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
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))

    def enter_email(self, email: str):
        email_field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_field.clear()
        email_field.send_keys(email)

    def enter_password(self, password: str):
        password_field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_button.click()

    def is_dashboard_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))
            return True
        except:
            return False

    def is_error_message_displayed(self, expected_message: str = None):
        try:
            error_element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            if expected_message:
                return expected_message in error_element.text
            return True
        except:
            return False

    def is_login_page_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
            self.wait.until(EC.visibility_of_element_located(self.LOGIN_BUTTON))
            return True
        except:
            return False

    def get_validation_error(self):
        try:
            validation_error = self.wait.until(EC.visibility_of_element_located(self.VALIDATION_ERROR))
            return validation_error.text
        except:
            return None

    def get_empty_field_prompt(self):
        try:
            prompt = self.wait.until(EC.visibility_of_element_located(self.EMPTY_FIELD_PROMPT))
            return prompt.text
        except:
            return None

    def is_user_profile_icon_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))
            return True
        except:
            return False
