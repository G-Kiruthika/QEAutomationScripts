import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):

    # Existing test methods...
    # (Assume all previous content remains unchanged)

    def test_TC_LOGIN_006_remember_me_auto_login(self):
        """TC_LOGIN_006: Valid login with 'Remember Me' checked, browser close/reopen, auto-login check."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login_with_remember_me(email="valid_user@example.com", password="valid_password")
        login_page.assert_user_logged_in()
        driver.quit()

        # Simulate browser reopen for auto-login check
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.navigate_to_home()
        login_page.assert_remember_me_auto_login()
        driver.quit()

    def test_TC_LOGIN_04_invalid_login_error(self):
        """TC-LOGIN-04: Invalid login with wrong email/password, error message validation."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login_with_invalid_credentials(email="wrong_user@example.com", password="wrong_password")
        login_page.assert_login_failed(expected_error="Invalid email or password.")
        driver.quit()

    def test_TC_LOGIN_007_forgot_password_flow(self):
        """TC_LOGIN_007: Forgot Password flow - submit password reset for registered email, verify confirmation."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        login_page.click_forgot_password_link()
        login_page.enter_forgot_password_email("user@example.com")
        login_page.submit_password_reset()
        confirmation_message = login_page.get_password_reset_confirmation()
        self.assertIsNotNone(confirmation_message, "Password reset confirmation message should be present.")
        self.assertIn("reset link has been sent", confirmation_message.lower(), "Confirmation message should indicate reset link sent.")
        driver.quit()

    def test_TC_LOGIN_05_login_with_empty_email(self):
        """TC-LOGIN-05: Login with empty email - verify error message indicating email is required."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        login_page.enter_email("")
        login_page.enter_password("ValidPassword123!")
        login_page.submit_login()
        # Check for empty field prompt or specific error message
        empty_prompt_present = login_page.is_empty_field_prompt_present()
        error_message = login_page.get_error_message()
        self.assertTrue(empty_prompt_present or (error_message and "email" in error_message.lower()), "Should show prompt or error message for empty email field.")
        driver.quit()
