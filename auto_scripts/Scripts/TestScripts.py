# TestScripts.py
# Selenium Test Scripts for Login Page

import pytest
from selenium import webdriver
from pages.login_page import LoginPage

LOGIN_URL = 'https://your-app-url/login'

@pytest.fixture(scope='module')
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# TC_LOGIN_001: Invalid login, error message validation
def test_invalid_login(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login_screen(LOGIN_URL)
    login_page.enter_username('invalidUser')
    login_page.enter_password('invalidPass')
    login_page.click_login_button()
    assert login_page.is_error_message_displayed(), "Error message for invalid login should be displayed."

# TC_LOGIN_002: Absence of 'Remember Me' checkbox
def test_remember_me_absence(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login_screen(LOGIN_URL)
    assert not login_page.is_remember_me_present(), "'Remember Me' checkbox should NOT be present on the login page."
