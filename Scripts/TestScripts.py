import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestScripts(unittest.TestCase):

    # Existing test methods...

    def test_TC_LOGIN_001_valid_login(self):
        """TC_LOGIN_001: Valid login with user@example.com/ValidPass123!"""
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.login('user@example.com', 'ValidPass123!')
            self.assertTrue(login_page.is_logged_in())
        finally:
            driver.quit()

    def test_TC_LOGIN_002_invalid_login(self):
        """TC_LOGIN_002: Invalid login with invaliduser@example.com/WrongPass!@#"""
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.login_invalid('invaliduser@example.com', 'WrongPass!@#')
            self.assertTrue(login_page.is_login_error_displayed())
        finally:
            driver.quit()

    def test_TC_LOGIN_003_empty_fields(self):
        """TC_LOGIN_003: Attempt login with empty fields and verify error handling."""
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.navigate()
            login_page.login_with_empty_fields()
            error_displayed = login_page.is_empty_field_prompt_displayed() or login_page.get_error_message() != ''
            self.assertTrue(error_displayed, "Error message or empty field prompt should be displayed.")
        finally:
            driver.quit()

    def test_TC_LOGIN_004_remember_me_persistence(self):
        """TC_LOGIN_004: Valid login with 'Remember Me' checked and session persistence after browser restart."""
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.navigate()
            login_page.login('user1', 'Pass@123', remember_me=True)
            self.assertTrue(login_page.is_dashboard_header_displayed() or login_page.is_user_profile_icon_displayed(), "User should be logged in.")
            # Simulate browser restart and session persistence
            driver.quit()
            driver2 = webdriver.Chrome()
            try:
                login_page2 = LoginPage(driver2)
                login_page2.navigate()
                try:
                    login_page2.verify_remember_me_functionality()
                except NotImplementedError:
                    # Placeholder: In actual implementation, validate cookies/session persistence here
                    pass
                # You may check for dashboard or profile icon again
                self.assertTrue(login_page2.is_dashboard_header_displayed() or login_page2.is_user_profile_icon_displayed(), "User should remain logged in after browser restart.")
            finally:
                driver2.quit()
        finally:
            try:
                driver.quit()
            except Exception:
                pass
