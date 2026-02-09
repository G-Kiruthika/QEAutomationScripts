import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

class LoginTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)

    # ... (existing test methods remain unchanged) ...

    def test_TC_LOGIN_05_min_length_input(self):
        ...
    def test_TC_LOGIN_06_special_char_input(self):
        ...
    def test_TC_LOGIN_07_sql_injection_xss(self):
        ...
    def test_TC_LOGIN_08_remember_me_session_persistence(self):
        ...

    def test_TC_LOGIN_09_forgot_password_workflow(self):
        """
        TC_LOGIN_09: Forgot Password workflow
        1. Navigate to login page
        2. Click 'Forgot Password'
        3. Enter registered email ('registered_user@example.com') and submit
        4. Assert password reset instructions are sent.
        """
        try:
            self.login_page.navigate_to_login()
            self.login_page.click_forgot_password()
            self.login_page.enter_email_for_reset('registered_user@example.com')
            self.login_page.submit_password_reset()
            # Robust assertion for reset instructions
            reset_message = self.login_page.get_reset_confirmation_message()
            self.assertIn("instructions", reset_message.lower(), "Password reset instructions not sent or not found in confirmation message.")
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"Forgot Password workflow failed due to exception: {str(e)}")
        except Exception as e:
            self.fail(f"Unexpected error in Forgot Password workflow: {str(e)}")

    def test_TC_LOGIN_10_multiple_failed_login_attempts(self):
        """
        TC_LOGIN_10: Multiple Failed Login Attempts/Account Lockout/CAPTCHA
        1. Navigate to login page
        2. Attempt login 5 times with invalid_user/invalid_pass
        3. Assert error after each attempt
        4. Assert account is locked or CAPTCHA is triggered after threshold.
        """
        try:
            self.login_page.navigate_to_login()
            error_messages = []
            for attempt in range(5):
                self.login_page.enter_username('invalid_user')
                self.login_page.enter_password('invalid_pass')
                self.login_page.submit_login()
                # Wait for error message
                time.sleep(1)
                error_msg = self.login_page.get_login_error_message()
                error_messages.append(error_msg)
                self.assertTrue(error_msg, f"No error message found after failed login attempt {attempt+1}.")
            # After 5 attempts, check for lockout or CAPTCHA
            lockout_msg = self.login_page.get_account_lockout_message()
            captcha_present = self.login_page.is_captcha_present()
            self.assertTrue(lockout_msg or captcha_present, "Account lockout or CAPTCHA not triggered after multiple failed attempts.")
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f"Multiple failed login attempts test failed due to exception: {str(e)}")
        except Exception as e:
            self.fail(f"Unexpected error in Multiple Failed Login Attempts test: {str(e)}")

if __name__ == "__main__":
    unittest.main()
