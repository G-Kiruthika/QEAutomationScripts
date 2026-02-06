from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.Locators import Locators

class LoginPage:
    """
    PageClass for automating login page interactions per TC-LOGIN-008.
    All locators are sourced from Locators.json. Methods are atomic and reusable.
    """
    URL = 'https://example-ecommerce.com/login'
    EMAIL_FIELD = (By.ID, 'login-email')
    PASSWORD_FIELD = (By.ID, 'login-password')
    REMEMBER_ME_CHECKBOX = (By.ID, 'remember-me')
    LOGIN_SUBMIT = (By.ID, 'login-submit')
    DASHBOARD_HEADER = (By.CSS_SELECTOR, 'h1.dashboard-title')
    USER_PROFILE_ICON = (By.CSS_SELECTOR, '.user-profile-name')
    ERROR_MESSAGE = (By.CSS_SELECTOR, 'div.alert-danger')
    VALIDATION_ERROR = (By.CSS_SELECTOR, '.invalid-feedback')
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def navigate_to_login_page(self):
        """Navigate to the login page URL."""
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.EMAIL_FIELD))

    def enter_email(self, email):
        """Enter email address."""
        email_elem = self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password):
        """Enter password."""
        password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_elem.clear()
        password_elem.send_keys(password)

    def is_remember_me_checked(self):
        """Return True if 'Remember Me' is checked, else False."""
        checkbox = self.wait.until(EC.presence_of_element_located(self.REMEMBER_ME_CHECKBOX))
        return checkbox.is_selected()

    def ensure_remember_me_unchecked(self):
        """Ensure 'Remember Me' checkbox is NOT checked."""
        checkbox = self.wait.until(EC.presence_of_element_located(self.REMEMBER_ME_CHECKBOX))
        if checkbox.is_selected():
            checkbox.click()

    def click_login(self):
        """Click the login button."""
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_SUBMIT))
        login_btn.click()

    def verify_dashboard_loaded(self):
        """Verify dashboard header is visible after login."""
        return self.wait.until(EC.visibility_of_element_located(self.DASHBOARD_HEADER))

    def verify_user_profile_icon(self):
        """Verify user profile icon is visible after login."""
        return self.wait.until(EC.visibility_of_element_located(self.USER_PROFILE_ICON))

    def close_browser(self):
        """Close the browser completely."""
        self.driver.quit()

    @staticmethod
    def reopen_browser(driver_class, options=None):
        """Reopen the browser (static utility, returns new driver instance)."""
        if options:
            return driver_class(options=options)
        return driver_class()

    def verify_login_page_displayed(self):
        """Verify login page is displayed (email field visible)."""
        return self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))

    def verify_session_not_persisted(self):
        """Verify user is redirected to login page (no session persistence)."""
        self.driver.get(self.URL)
        return self.verify_login_page_displayed()

    # --- New methods for TC-LOGIN-009 ---
    def is_forgot_password_link_present_and_clickable(self):
        """
        Verifies that the 'Forgot Password' link is present and clickable on the login page.
        Returns True if present and clickable, False otherwise.
        """
        try:
            forgot_password_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.forgot-password-link')))
            return forgot_password_link.is_displayed() and forgot_password_link.is_enabled()
        except Exception:
            return False

    def click_forgot_password_link(self):
        """
        Clicks the 'Forgot Password' link on the login page.
        """
        forgot_password_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.forgot-password-link')))
        forgot_password_link.click()

    def verify_password_recovery_page_elements(self):
        """
        Verifies that the password recovery page displays the email input field and submit button.
        Returns True if both elements are present and displayed, False otherwise.
        """
        try:
            email_input = self.wait.until(EC.visibility_of_element_located((By.ID, 'recovery-email')))
            submit_button = self.wait.until(EC.visibility_of_element_located((By.ID, 'recovery-submit')))
            return email_input.is_displayed() and submit_button.is_displayed()
        except Exception:
            return False
