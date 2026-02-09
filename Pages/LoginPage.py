# LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    """
    Page Object for Login Page.
    Implements actions and verifications for login scenarios.
    """
    # Locators (from Locators.json)
    EMAIL_INPUT = (By.ID, 'login-email')
    PASSWORD_INPUT = (By.ID, 'login-password')
    REMEMBER_ME_CHECKBOX = (By.ID, 'remember-me')
    LOGIN_BUTTON = (By.ID, 'login-submit')
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, 'a.forgot-password-link')
    ERROR_MESSAGE = (By.CSS_SELECTOR, 'div.alert-danger')
    VALIDATION_ERROR = (By.CSS_SELECTOR, '.invalid-feedback')
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[contains(text,'Mandatory fields are required')]")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, 'h1.dashboard-title')
    USER_PROFILE_ICON = (By.CSS_SELECTOR, '.user-profile-name')

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def navigate_to_login_page(self, url: str = 'https://example-ecommerce.com/login'):
        """Navigate to the login page."""
        self.driver.get(url)

    def enter_email(self, email: str):
        """Enter email into the email field."""
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        email_field.clear()
        email_field.send_keys(email)

    def enter_password(self, password: str):
        """Enter password into the password field."""
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)

    def leave_password_empty(self):
        """Ensure the password field is empty."""
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()

    def click_login_button(self):
        """Click the login button."""
        login_btn = self.driver.find_element(*self.LOGIN_BUTTON)
        login_btn.click()

    def is_login_page_displayed(self) -> bool:
        """Verify if login page is displayed."""
        return self.driver.find_element(*self.EMAIL_INPUT).is_displayed() and \
               self.driver.find_element(*self.PASSWORD_INPUT).is_displayed()

    def is_email_field_empty(self) -> bool:
        """Check if the email field is empty."""
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        return email_field.get_attribute('value') == ''

    def is_password_field_empty(self) -> bool:
        """Check if the password field is empty."""
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        return password_field.get_attribute('value') == ''

    def is_email_accepted(self, expected_email: str) -> bool:
        """Verify if email is accepted (entered correctly)."""
        email_field = self.driver.find_element(*self.EMAIL_INPUT)
        return email_field.get_attribute('value') == expected_email

    def is_validation_error_displayed(self) -> bool:
        """Check if validation error is displayed (for min/max length)."""
        try:
            validation_error = self.driver.find_element(*self.VALIDATION_ERROR)
            return validation_error.is_displayed()
        except Exception:
            return False

    def get_validation_error_text(self) -> str:
        """Get the validation error text."""
        try:
            validation_error = self.driver.find_element(*self.VALIDATION_ERROR)
            return validation_error.text
        except Exception:
            return ''

    def is_error_message_displayed(self) -> bool:
        """Check if error message is displayed (general errors)."""
        try:
            error_msg = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_msg.is_displayed()
        except Exception:
            return False

    def get_error_message_text(self) -> str:
        """Get the error message text."""
        try:
            error_msg = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_msg.text
        except Exception:
            return ''

    def is_empty_field_prompt_displayed(self) -> bool:
        """Check if empty field prompt is displayed (password required)."""
        try:
            prompt = self.driver.find_element(*self.EMPTY_FIELD_PROMPT)
            return prompt.is_displayed()
        except Exception:
            return False

    def is_user_logged_in(self) -> bool:
        """Check if user is successfully logged in (e.g., dashboard header displayed)."""
        try:
            dashboard_header = self.driver.find_element(*self.DASHBOARD_HEADER)
            return dashboard_header.is_displayed()
        except Exception:
            return False

    # --- Appended for TC-LOGIN-08 ---
    def select_remember_me(self):
        """Select the 'Remember Me' checkbox if not already selected."""
        checkbox = self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
        if not checkbox.is_selected():
            checkbox.click()

    def is_remember_me_selected(self) -> bool:
        """Check if the 'Remember Me' checkbox is selected."""
        checkbox = self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
        return checkbox.is_selected()

    def verify_session_persistence(self) -> bool:
        """
        Stub method for session persistence verification after browser restart.
        Actual implementation should be handled in test scripts.
        """
        # This method can be called after reopening browser and navigating to app
        try:
            return self.is_user_logged_in()
        except Exception:
            return False
