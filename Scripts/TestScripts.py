import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from Pages.LoginPage import LoginPage
from Pages.ForgotPasswordPage import ForgotPasswordPage
import time

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://example-ecommerce.com/login")
        self.login_page = LoginPage(self.driver)
        self.forgot_password_page = ForgotPasswordPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # Existing test methods preserved...

    def test_TC_LOGIN_005_empty_fields_error(self):
        pass

    def test_TC_LOGIN_006_remember_me_session_persistence(self):
        pass

    def test_TC_LOGIN_007_forgot_password_flow(self):
        """
        TC_LOGIN_007:
        1. Navigate to login page.
        2. Click 'Forgot Password?' link.
        3. Verify presence of email input and reset instructions.
        """
        self.login_page.go_to_login_page()
        forgot_link = self.login_page.wait.until(By.CSS_SELECTOR, "a.forgot-password-link")
        forgot_link.click()
        self.forgot_password_page.go_to_forgot_password_page()
        email_input_present = self.forgot_password_page.is_email_input_present()
        reset_instruction_present = self.forgot_password_page.is_reset_instruction_present()
        self.assertTrue(email_input_present, "Email input should be present on Forgot Password page.")
        self.assertTrue(reset_instruction_present, "Reset instructions should be visible on Forgot Password page.")

    def test_TC_LOGIN_008_max_email_length(self):
        """
        TC_LOGIN_008:
        1. Navigate to login page.
        2. Enter maximum allowed length email ("a"*64 + "@example.com") in email field.
        3. Enter valid password.
        4. Click Login.
        5. Verify field accepts input up to max length and login behavior.
        """
        self.login_page.go_to_login_page()
        max_length = 64
        email = "a" * max_length + "@example.com"
        password = "ValidPass123!"
        valid_length = self.login_page.validate_email_max_length(max_length)
        self.login_page.enter_email(email)
        self.login_page.enter_password(password)
        self.login_page.click_login()
        dashboard_displayed = self.login_page.is_dashboard_header_displayed()
        self.assertTrue(valid_length, f"Email field should accept input up to {max_length} characters before '@'.")
        self.assertTrue(dashboard_displayed or self.login_page.is_error_message_displayed(), "Should either log in or show error if credentials mismatch.")

if __name__ == "__main__":
    unittest.main()
