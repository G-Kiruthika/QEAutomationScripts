import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class LoginTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)

    # ... (existing test methods remain unchanged) ...

    def test_TC_LOGIN_05_min_length_input(self):
        """
        TC_LOGIN_05: Enter minimum length (1 char) for username and password. Assert min length error is displayed.
        """
        try:
            self.login_page.open()
            self.login_page.enter_email('a')
            self.login_page.enter_password('b')
            self.login_page.click_login()
            error_displayed = self.login_page.is_min_length_error_displayed()
            self.assertTrue(error_displayed, 'Minimum length error should be displayed for 1-char credentials.')
        except Exception as e:
            self.fail(f"Exception occurred in TC_LOGIN_05: {e}")
        finally:
            self.driver.quit()

    def test_TC_LOGIN_06_special_char_input(self):
        """
        TC_LOGIN_06: Enter special characters for username and password. Assert input is accepted or handled.
        """
        try:
            self.login_page.open()
            username = 'user!@#'
            password = 'pass$%^'
            self.login_page.enter_email(username)
            self.login_page.enter_password(password)
            input_accepted = self.login_page.is_special_char_input_accepted(username, password)
            self.assertTrue(input_accepted, 'Special character input should be accepted or handled appropriately.')
            self.login_page.click_login()
        except Exception as e:
            self.fail(f"Exception occurred in TC_LOGIN_06: {e}")
        finally:
            self.driver.quit()

    def test_TC_LOGIN_07_sql_injection_xss(self):
        """
        TC_LOGIN_07: Validate resistance to SQL injection/XSS by entering username: "' OR 1=1;" and password: "<script>alert('XSS')</script>", clicking login, and asserting that an error message is displayed and no injection occurs.
        """
        try:
            self.login_page.open()
            self.login_page.enter_email("' OR 1=1;")
            self.login_page.enter_password("<script>alert('XSS')</script>")
            self.login_page.click_login()
            error_message = self.login_page.get_error_message()
            self.assertIsNotNone(error_message, "Error message should be displayed for SQL injection/XSS input.")
            self.assertIn("error", error_message.lower(), "Application should remain secure and display an error.")
        except Exception as e:
            self.fail(f"Exception occurred in TC_LOGIN_07: {e}")
        finally:
            self.driver.quit()

    def test_TC_LOGIN_08_remember_me_session_persistence(self):
        """
        TC_LOGIN_08: Validate 'Remember Me' by logging in with username: "valid_user", password: "valid_pass", checking 'Remember Me', saving cookies, restarting browser, restoring cookies, and asserting session persistence.
        """
        try:
            self.login_page.open()
            self.login_page.enter_email("valid_user")
            self.login_page.enter_password("valid_pass")
            self.login_page.click_remember_me()
            self.login_page.click_login()
            cookies = self.driver.get_cookies()
            self.driver.quit()
            self.driver = webdriver.Chrome()
            self.login_page = LoginPage(self.driver)
            self.driver.get("https://example-ecommerce.com/login")
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            session_persistent = self.login_page.is_session_persistent(cookies)
            self.assertTrue(session_persistent, "Session should persist after browser restart when 'Remember Me' is checked.")
        except Exception as e:
            self.fail(f"Exception occurred in TC_LOGIN_08: {e}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()
