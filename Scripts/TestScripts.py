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
            # Optionally check input acceptance if such a method exists; otherwise proceed
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
            # Check input acceptance (assumes method returns True if accepted, False otherwise)
            input_accepted = self.login_page.is_special_char_input_accepted(username, password)
            self.assertTrue(input_accepted, 'Special character input should be accepted or handled appropriately.')
            self.login_page.click_login()
            # Depending on expected behavior, add further asserts here if needed
        except Exception as e:
            self.fail(f"Exception occurred in TC_LOGIN_06: {e}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()
