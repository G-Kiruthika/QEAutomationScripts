
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