
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from Pages.LoginPage import LoginPage
import time

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://your-app-url.com")
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    # Existing test methods preserved...

    def test_TC_LOGIN_005_empty_fields_error(self):
        """
        TC_LOGIN_005: 
        1. Navigate to login page.
        2. Leave both fields empty.
        3. Click Login.
        Expect: Error messages 'Email is required.' and 'Password is required.' User not logged in.
        """
        self.login_page.navigate_to_login()
        self.login_page.enter_email("")
        self.login_page.enter_password("")
        self.login_page.click_login()
        email_error = self.login_page.get_email_error()
        password_error = self.login_page.get_password_error()
        self.assertEqual(email_error, "Email is required.")
        self.assertEqual(password_error, "Password is required.")
        self.assertFalse(self.login_page.is_logged_in())

    def test_TC_LOGIN_006_remember_me_session_persistence(self):
        """
        TC_LOGIN_006:
        1. Navigate to login page.
        2. Enter valid email/password (user@example.com/ValidPass123!).
        3. Check 'Remember Me'.
        4. Click Login.
        5. Close and reopen browser, revisit site.
        Expect: User remains logged in. Session persists.
        """
        self.login_page.navigate_to_login()
        self.login_page.enter_email("user@example.com")
        self.login_page.enter_password("ValidPass123!")
        self.login_page.check_remember_me()
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_logged_in())

        # Simulate browser restart
        cookies = self.driver.get_cookies()
        self.driver.quit()
        time.sleep(2)  # Wait for browser to close

        self.driver = webdriver.Chrome()
        self.driver.get("https://your-app-url.com")
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        self.login_page = LoginPage(self.driver)
        self.assertTrue(self.login_page.is_logged_in())

if __name__ == "__main__":
    unittest.main()
