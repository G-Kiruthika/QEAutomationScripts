# Existing imports (unchanged)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    # Locators (updated per metadata, using placeholder values)
    username_field = (By.PLACEHOLDER, 'placeholder_locator_username_field')
    password_field = (By.PLACEHOLDER, 'placeholder_locator_password_field')
    login_button = (By.PLACEHOLDER, 'placeholder_locator_login_button')
    error_message = (By.PLACEHOLDER, 'placeholder_locator_error_message')

    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Action methods (all per metadata)
    def navigate_to_login_page(self, url):
        self.driver.get(url)

    def enter_username(self, username):
        self.driver.find_element(*self.username_field).clear()
        self.driver.find_element(*self.username_field).send_keys(username)

    def leave_username_empty(self):
        self.driver.find_element(*self.username_field).clear()

    def enter_password(self, password):
        self.driver.find_element(*self.password_field).clear()
        self.driver.find_element(*self.password_field).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()

    # Validation methods (all per metadata)
    def verify_error_message(self, expected_message):
        actual_message = self.driver.find_element(*self.error_message).text
        assert actual_message == expected_message, f"Expected '{expected_message}', got '{actual_message}'"

    def verify_login_prevented(self):
        assert self.driver.current_url.endswith("/login"), "Login was not prevented."

    def verify_account_lockout_notification(self):
        lockout_element = self.driver.find_elements(By.PLACEHOLDER, "lockout-notification")
        assert lockout_element and lockout_element[0].is_displayed(), "Account lockout notification not displayed."
