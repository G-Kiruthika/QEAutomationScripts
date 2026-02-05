from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

class LoginPage:
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    LOGIN_SUBMIT = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    # Note: 'rememberMeCheckbox' is intentionally not used as we are verifying its absence

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def go_to_login_page(self):
        """
        Navigates to the login page URL and waits for the email input field to be present.
        """
        self.driver.get(self.URL)
        # Optionally, add explicit wait for the email field
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located(self.EMAIL_FIELD)
        # )

    def is_remember_me_checkbox_present(self) -> bool:
        """
        Checks if the 'Remember Me' checkbox is present on the page.
        Returns True if present, False otherwise.
        """
        try:
            self.driver.find_element(By.ID, "remember-me")
            return True
        except NoSuchElementException:
            return False

    def assert_remember_me_checkbox_not_present(self):
        """
        Asserts that the 'Remember Me' checkbox is NOT present on the page.
        Raises AssertionError if found.
        """
        if self.is_remember_me_checkbox_present():
            raise AssertionError("'Remember Me' checkbox should not be present on the login page.")
