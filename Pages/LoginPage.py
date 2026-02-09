# LoginPage.py
"""
Page Object Model for the Login Page
Author: [Your Name]
Description: This class encapsulates the interactions and verifications for the Login Page,
using locators defined in Locators.json. It includes methods to navigate to the login screen,
enter credentials, submit login, verify dashboard, verify error messages, handle 'Forgot Password',
and accessibility checks (screen reader, keyboard navigation, color contrast), plus password masking verification.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class LoginPage:
    """
    Page Object for the Login Screen
    """

    # Locators (from Locators.json)
    URL = "https://example-ecommerce.com/login"
    EMAIL_FIELD = (By.ID, "login-email")
    PASSWORD_FIELD = (By.ID, "login-password")
    REMEMBER_ME_CHECKBOX = (By.ID, "remember-me")
    LOGIN_SUBMIT_BUTTON = (By.ID, "login-submit")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a.forgot-password-link")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".invalid-feedback")
    EMPTY_FIELD_PROMPT = (By.XPATH, "//*[text()='Mandatory fields are required']")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")
    PASSWORD_RECOVERY_HEADER = (By.CSS_SELECTOR, "h1.password-recovery-title") # Add locator for password recovery page header if available

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initializes the LoginPage with a Selenium WebDriver instance.
        :param driver: Selenium WebDriver
        :param timeout: Default wait timeout for elements
        """
        self.driver = driver
        self.timeout = timeout

    def go_to_login_page(self):
        """
        Navigates the browser to the login page URL and waits for the login form to be visible.
        """
        self.driver.get(self.URL)
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD),
            message="Login email field not visible after navigating to login page."
        )

    def enter_username(self, username: str):
        """
        Enters the username (email) into the email field.
        """
        email_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.EMAIL_FIELD)
        )
        email_input.clear()
        email_input.send_keys(username)

    def enter_password(self, password: str):
        """
        Enters the password into the password field.
        """
        password_input = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.PASSWORD_FIELD)
        )
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        """
        Clicks the login button to submit credentials.
        """
        login_button = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.LOGIN_SUBMIT_BUTTON)
        )
        login_button.click()

    def is_dashboard_displayed(self) -> bool:
        """
        Checks if the dashboard header is displayed after successful login.
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.DASHBOARD_HEADER)
            )
            return True
        except Exception:
            return False

    def is_error_message_displayed(self) -> bool:
        """
        Checks if error message is displayed after invalid login.
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return True
        except Exception:
            return False

    def is_remember_me_checkbox_present(self) -> bool:
        """
        Checks if the 'Remember Me' checkbox is present on the login page.
        :return: True if present, False otherwise
        """
        try:
            self.driver.find_element(*self.REMEMBER_ME_CHECKBOX)
            return True
        except NoSuchElementException:
            return False

    def assert_remember_me_checkbox_absent(self):
        """
        Asserts that the 'Remember Me' checkbox is NOT present on the login page.
        Raises AssertionError if the checkbox is found.
        """
        if self.is_remember_me_checkbox_present():
            raise AssertionError(
                "'Remember Me' checkbox should NOT be present on the Login Page, but it was found."
            )

    def get_error_message_text(self) -> str:
        """
        Returns the error message text displayed for invalid login.
        """
        try:
            error_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error_elem.text
        except Exception:
            return ""

    # NEW METHODS ADDED FOR TC_LOGIN_005 AND TC_LOGIN_006
    def click_forgot_password(self):
        """
        Clicks the 'Forgot Password' link on the login page.
        """
        forgot_link = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK)
        )
        forgot_link.click()

    def is_password_recovery_page_displayed(self) -> bool:
        """
        Checks if the password recovery page is displayed after clicking 'Forgot Password'.
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.PASSWORD_RECOVERY_HEADER)
            )
            return True
        except Exception:
            return False

    def attempt_sql_injection_login(self, username: str, password: str) -> bool:
        """
        Attempts login with SQL injection strings and verifies that login fails (no unauthorized access).
        Returns True if login fails and no dashboard is displayed.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        error_displayed = self.is_error_message_displayed()
        dashboard_displayed = self.is_dashboard_displayed()
        return error_displayed and not dashboard_displayed

    # ----------- NEW METHODS FOR ACCESSIBILITY & PASSWORD MASKING -----------
    def is_login_page_accessible(self) -> dict:
        """
        Checks accessibility features: screen reader compatibility (aria attributes),
        keyboard navigation (tab order), and color contrast (basic CSS check).
        Returns a dict summarizing the checks.
        """
        results = {
            'screen_reader_compatible': False,
            'keyboard_navigation': False,
            'color_contrast': False
        }
        # Screen reader compatibility: check for aria-label/aria-describedby on form fields
        email_elem = self.driver.find_element(*self.EMAIL_FIELD)
        password_elem = self.driver.find_element(*self.PASSWORD_FIELD)
        login_btn = self.driver.find_element(*self.LOGIN_SUBMIT_BUTTON)
        aria_email = email_elem.get_attribute('aria-label') or email_elem.get_attribute('aria-describedby')
        aria_password = password_elem.get_attribute('aria-label') or password_elem.get_attribute('aria-describedby')
        aria_login_btn = login_btn.get_attribute('aria-label') or login_btn.get_attribute('aria-describedby')
        results['screen_reader_compatible'] = bool(aria_email and aria_password and aria_login_btn)

        # Keyboard navigation: try tabbing through fields
        try:
            email_elem.click()
            email_elem.send_keys(Keys.TAB)
            focused_elem = self.driver.switch_to.active_element
            # Should focus password field
            results['keyboard_navigation'] = focused_elem == password_elem
        except Exception:
            results['keyboard_navigation'] = False

        # Color contrast: basic check using JS to compare foreground/background colors
        try:
            color_contrast_js = """
                function luminance(r, g, b) {
                    var a = [r, g, b].map(function(v) {
                        v = v / 255;
                        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
                    });
                    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
                }
                function contrast(rgb1, rgb2) {
                    var lum1 = luminance(rgb1[0], rgb1[1], rgb1[2]);
                    var lum2 = luminance(rgb2[0], rgb2[1], rgb2[2]);
                    var brightest = Math.max(lum1, lum2);
                    var darkest = Math.min(lum1, lum2);
                    return (brightest + 0.05) / (darkest + 0.05);
                }
                function getRGB(elem, prop) {
                    var color = window.getComputedStyle(elem)[prop];
                    var match = color.match(/rgb\((\d+), (\d+), (\d+)\)/);
                    if (match) {
                        return [parseInt(match[1]), parseInt(match[2]), parseInt(match[3])];
                    }
                    return [0,0,0];
                }
                var elem = arguments[0];
                var fg = getRGB(elem, 'color');
                var bg = getRGB(elem, 'backgroundColor');
                return contrast(fg, bg);
            """
            email_contrast = self.driver.execute_script(color_contrast_js, email_elem)
            password_contrast = self.driver.execute_script(color_contrast_js, password_elem)
            login_btn_contrast = self.driver.execute_script(color_contrast_js, login_btn)
            # WCAG recommends contrast ratio >= 4.5 for normal text
            results['color_contrast'] = all([email_contrast >= 4.5, password_contrast >= 4.5, login_btn_contrast >= 4.5])
        except Exception:
            results['color_contrast'] = False
        return results

    def is_password_masked(self) -> bool:
        """
        Verifies that the password input field masks input (type='password').
        """
        password_elem = self.driver.find_element(*self.PASSWORD_FIELD)
        return password_elem.get_attribute('type') == 'password'

# Example usage for new test cases:
# def test_login_accessibility(driver):
#     login_page = LoginPage(driver)
#     login_page.go_to_login_page()
#     accessibility = login_page.is_login_page_accessible()
#     assert accessibility['screen_reader_compatible'], "Screen reader compatibility failed."
#     assert accessibility['keyboard_navigation'], "Keyboard navigation failed."
#     assert accessibility['color_contrast'], "Color contrast failed."
#
# def test_password_masking(driver):
#     login_page = LoginPage(driver)
#     login_page.go_to_login_page()
#     login_page.enter_password('Pass@123')
#     assert login_page.is_password_masked(), "Password is not masked."
