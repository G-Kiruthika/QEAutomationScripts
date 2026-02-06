# LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LoginPage:
    LOGIN_URL = "https://example-ecommerce.com/login"
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

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to_login_page(self):
        self.driver.get(self.LOGIN_URL)
        # Wait for login screen to be displayed
        self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))

    def assert_remember_me_checkbox_absent(self):
        # Should raise AssertionError if checkbox is present
        try:
            self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
            raise AssertionError("'Remember Me' checkbox is present, but should NOT be.")
        except NoSuchElementException:
            # Correct behavior: checkbox is absent
            pass
        except Exception as e:
            raise AssertionError(f"Unexpected error during checkbox absence check: {e}")

    # Additional methods for completeness (not used in TC_LOGIN_002)
    def is_login_screen_displayed(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))
            self.wait.until(EC.presence_of_element_located(self.PASSWORD_FIELD))
            self.wait.until(EC.presence_of_element_located(self.LOGIN_SUBMIT))
            return True
        except TimeoutException:
            return False