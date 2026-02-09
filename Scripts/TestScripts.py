import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):

    # Existing test methods...
    # (Assume all previous content remains unchanged)

    def test_TC_LOGIN_006_remember_me_auto_login(self):
        ...
    def test_TC_LOGIN_04_invalid_login_error(self):
        ...
    def test_TC_LOGIN_007_forgot_password_flow(self):
        ...
    def test_TC_LOGIN_05_login_with_empty_email(self):
        ...
    def test_TC_LOGIN_009_password_length_validation(self):
        ...
    def test_TC_LOGIN_07_login_with_empty_fields(self):
        ...
    def test_TC_LOGIN_010_special_char_login(self):
        ...
    def test_TC_LOGIN_08_remember_me_session_persistence(self):
        ...
    def test_TC_LOGIN_09_max_length_email(self):
        ...
    def test_TC_LOGIN_10_sql_injection(self):
        ...

    def test_TC_LOGIN_001_valid_login(self):
        """TC_LOGIN_001: Valid login with user@example.com / validPassword123"""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.open()
        login_page.enter_email("user@example.com")
        login_page.enter_password("validPassword123")
        login_page.click_login()
        logged_in = login_page.is_dashboard_header_displayed()
        self.assertTrue(logged_in, "User should be logged in and redirected to dashboard/home page.")
        driver.quit()

    def test_TC_LOGIN_002_invalid_login(self):
        """TC_LOGIN_002: Invalid login with wronguser@example.com / wrongPassword"""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.open()
        login_page.enter_email("wronguser@example.com")
        login_page.enter_password("wrongPassword")
        login_page.click_login()
        error_message = login_page.get_error_message()
        self.assertEqual(error_message, "Invalid credentials.", "Error message should be 'Invalid credentials.' for invalid login.")
        driver.quit()

    def test_TC_LOGIN_007_forgot_password(self):
        """TC_LOGIN_007: Navigate to login page and click 'Forgot Password' link, expect redirect."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.open()
        login_page.click_forgot_password()
        # Here, you would check that the URL or page content matches the Forgot Password page
        # For demonstration, let's check the current URL contains 'forgot-password'
        current_url = driver.current_url
        self.assertIn("forgot-password", current_url, "User should be redirected to the 'Forgot Password' page.")
        driver.quit()

    def test_TC_LOGIN_008_min_length_email_validation(self):
        """TC_LOGIN_008: Enter email below min length and valid password, expect error message."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.open()
        login_page.enter_email("ab")
        login_page.enter_password("validPassword123")
        login_page.click_login()
        validation_error = login_page.get_validation_error()
        self.assertEqual(validation_error, "Email/Username must be at least 3 characters.", "Validation error message should be displayed for min length email.")
        driver.quit()
