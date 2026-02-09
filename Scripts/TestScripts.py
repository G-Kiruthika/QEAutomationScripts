import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_login_valid_credentials(self):
        # Existing test method example
        self.login_page.navigate_to_login()
        self.login_page.enter_username('valid_user')
        self.login_page.enter_password('valid_pass')
        self.login_page.click_login()
        self.assertTrue(self.login_page.is_login_successful())

    def test_login_invalid_credentials(self):
        # Existing test method example
        self.login_page.navigate_to_login()
        self.login_page.enter_username('invalid_user')
        self.login_page.enter_password('invalid_pass')
        self.login_page.click_login()
        self.assertFalse(self.login_page.is_login_successful())

    # TC_LOGIN_005: Forgot Password navigation
    def test_forgot_password_navigation(self):
        """
        TC_LOGIN_005: Verify that clicking 'Forgot Password' navigates to the password recovery page
        Steps:
        1. Navigate to login page
        2. Click 'Forgot Password' link
        3. Assert navigation to password recovery page
        """
        self.login_page.navigate_to_login()
        result = self.login_page.click_forgot_password_and_validate_navigation()
        self.assertTrue(result, "Failed to navigate to password recovery page after clicking 'Forgot Password'.")

    # TC_LOGIN_006: SQL injection negative test
    def test_sql_injection_login_failure(self):
        """
        TC_LOGIN_006: Verify that SQL injection strings in login fields do not allow unauthorized access
        Steps:
        1. Navigate to login page
        2. Enter SQL injection strings in username and password
        3. Click login
        4. Assert login fails and no unauthorized access occurs
        """
        self.login_page.navigate_to_login()
        result = self.login_page.attempt_sql_injection_and_validate_failure(username="' OR 1=1; --", password="' OR 1=1; --")
        self.assertTrue(result, "SQL injection attempt did not fail as expected or unauthorized access occurred.")

if __name__ == "__main__":
    unittest.main()
