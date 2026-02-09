
import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):

    # Existing test methods...
    def test_TC_LOGIN_006_remember_me_auto_login(self):
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        login_page.login_with_remember_me(email="valid_user@example.com", password="valid_password")
        login_page.assert_user_logged_in()
        driver.quit()
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.navigate_to_home()
        login_page.assert_remember_me_auto_login()
        driver.quit()

    def test_TC_LOGIN_04_invalid_login_error(self):
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        login_page.login_with_invalid_credentials(email="wrong_user@example.com", password="wrong_password")
        login_page.assert_login_failed(expected_error="Invalid email or password.")
        driver.quit()

    def test_TC_LOGIN_007_password_reset(self):
        """TC_LOGIN_007: Forgot Password flow for registered user."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        self.assertTrue(login_page.click_forgot_password())
        self.assertTrue(login_page.enter_email_for_reset("user@example.com"))
        confirmation = login_page.submit_password_reset()
        self.assertIsNotNone(confirmation)
        self.assertIn("Confirmation", confirmation.text)
        driver.quit()

    def test_TC_LOGIN_05_email_required_error(self):
        """TC-LOGIN-05: Login with empty email field and valid password, expect email required error."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        self.assertTrue(login_page.leave_email_empty())
        self.assertTrue(login_page.enter_password("ValidPassword123!"))
        self.assertTrue(login_page.click_login())
        error = login_page.get_email_required_error()
        self.assertIsNotNone(error)
        self.assertIn("Mandatory fields are required", error)
        driver.quit()
