import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

class LoginTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)

    # ... (other test methods, unchanged) ...

    def test_TC_LOGIN_09_forgot_password_workflow(self):
        """
        TC_LOGIN_09: Forgot Password workflow
        1. Navigate to login page
        2. Click 'Forgot Password'
        3. Enter registered email ('registered_user@example.com') and submit
        4. Assert password reset instructions are sent.
        """
        try:
            self.login_page.open()
            self.login_page.click_forgot_password()
            self.login_page.enter_reset_email('registered_user@example.com')
            self.login_page.submit_reset_request()
            self.assertTrue(
                self.login_page.is_reset_confirmation_displayed(),
                'Password reset confirmation not displayed.'
            )
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f'Forgot Password workflow failed due to exception: {str(e)}')
        except Exception as e:
            self.fail(f'Unexpected error in Forgot Password workflow: {str(e)}')

    def test_TC_LOGIN_10_multiple_failed_login_attempts(self):
        """
        TC_LOGIN_10: Multiple Failed Login Attempts/Account Lockout/CAPTCHA
        1. Navigate to login page
        2. Attempt login 5 times with invalid_user/invalid_pass
        3. Assert error after each attempt
        4. Assert account is locked or CAPTCHA is triggered after threshold.
        """
        try:
            self.login_page.open()
            self.login_page.attempt_invalid_login('invalid_user', 'invalid_pass', attempts=5)
            account_locked = self.login_page.is_account_locked()
            captcha_displayed = self.login_page.is_captcha_displayed()
            self.assertTrue(
                account_locked or captcha_displayed,
                'Account lockout or CAPTCHA not triggered after multiple failed attempts.'
            )
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f'Multiple failed login attempts test failed due to exception: {str(e)}')
        except Exception as e:
            self.fail(f'Unexpected error in Multiple Failed Login Attempts test: {str(e)}')

    def test_TC_LOGIN_03_empty_fields_validation(self):
        """
        TC_LOGIN_03: Empty Fields Validation
        1. Navigate to login page
        2. Leave username and password fields empty
        3. Click the 'Login' button
        4. Assert error message displayed: 'Fields cannot be empty'.
        """
        try:
            self.login_page.open()
            result = self.login_page.login_with_empty_fields()
            self.assertIsNotNone(result, 'No error or prompt message returned for empty fields.')
            self.assertIn('empty', result.lower(), f'Expected "Fields cannot be empty" error, got: {result}')
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f'Empty fields validation test failed due to exception: {str(e)}')
        except Exception as e:
            self.fail(f'Unexpected error in Empty Fields Validation test: {str(e)}')

    def test_TC_LOGIN_04_maximum_input_length(self):
        """
        TC_LOGIN_04: Maximum Input Length Validation
        1. Navigate to login page
        2. Enter username and password with maximum allowed characters (50)
        3. Click the 'Login' button
        4. Assert login succeeds or fails as per credentials validity.
        """
        try:
            self.login_page.open()
            max_username = 'a' * 50
            max_password = 'b' * 50
            result = self.login_page.login_with_max_input(max_username, max_password)
            self.assertIn('login_success', result, 'Result missing login_success key.')
            # Accept both success or error, but ensure error_message is handled
            if not result['login_success']:
                self.assertIsNotNone(result['error_message'], 'No error message for maximum input.')
        except (NoSuchElementException, TimeoutException) as e:
            self.fail(f'Maximum input length test failed due to exception: {str(e)}')
        except Exception as e:
            self.fail(f'Unexpected error in Maximum Input Length test: {str(e)}')

if __name__ == '__main__':
    unittest.main()
