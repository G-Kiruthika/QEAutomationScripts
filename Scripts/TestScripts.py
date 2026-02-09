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
            # Assert successful login, e.g., check for dashboard element
            self.assertTrue(login_page.is_logged_in())
        finally:
            driver.quit()

    def test_TC_LOGIN_002_invalid_login(self):
        """TC_LOGIN_002: Invalid login with invaliduser@example.com/WrongPass!@#"""
        driver = webdriver.Chrome()
        try:
            login_page = LoginPage(driver)
            login_page.login_invalid('invaliduser@example.com', 'WrongPass!@#')
            # Assert login failed, e.g., check for error message
            self.assertTrue(login_page.is_login_error_displayed())
        finally:
            driver.quit()
