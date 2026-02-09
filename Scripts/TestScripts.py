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
        login_page.go_to_login_page()
        login_page.enter_email("user@example.com")
        login_page.enter_password("validPassword123")
        login_page.click_login()
        logged_in = login_page.is_logged_in()
        self.assertTrue(logged_in, "User should be logged in and redirected to dashboard/home page.")
        driver.quit()

    def test_TC_LOGIN_002_invalid_login(self):
        """TC_LOGIN_002: Invalid login with wronguser@example.com / wrongPassword"""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        login_page.enter_email("wronguser@example.com")
        login_page.enter_password("wrongPassword")
        login_page.click_login()
        error_message = login_page.get_login_error_message()
        self.assertEqual(error_message, "Invalid credentials.", "Error message should be 'Invalid credentials.' for invalid login.")
        driver.quit()

    # --- Appended Methods for TC_LOGIN_007 and TC_LOGIN_008 ---
    def test_TC_LOGIN_007_forgot_password_link(self):
        """TC_LOGIN_007: Navigate to login page and click 'Forgot Password' link."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        self.assertTrue(login_page.is_login_page_displayed(), "Login page should be displayed.")
        login_page.click_forgot_password_link()
        # Here you may check for redirection, e.g., by URL or page element, but as per PageObject, assume redirection occurs
        # For demo, just check we are no longer on the login page
        self.assertFalse(login_page.is_login_page_displayed(), "User should be redirected from login page after clicking 'Forgot Password'.")
        driver.quit()

    def test_TC_LOGIN_008_min_length_email_validation(self):
        """TC_LOGIN_008: Enter email below minimum length and valid password, expect error message."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        self.assertTrue(login_page.is_login_page_displayed(), "Login page should be displayed.")
        # Step 2: Enter short email/username and valid password
        email_ok = login_page.email_field_accepts_input("ab")
        password_ok = login_page.password_field_accepts_input("validPassword123")
        self.assertTrue(email_ok, "Email/username field should accept input 'ab'.")
        self.assertTrue(password_ok, "Password field should accept input 'validPassword123'.")
        # Step 3: Click Login
        login_page.click_login()
        # Step 4: Error message check
        error_message = login_page.get_min_length_error_message()
        self.assertEqual(error_message, "Email/Username must be at least 3 characters.", "Should show min length validation error.")
        driver.quit()
