from selenium.webdriver.common.by import By
import pytest
from core.driver_factory import get_driver
from pages.login_page import LoginPage


def test_login_empty_username_validation():
    """TC_LOGIN_008: Verify login validation with empty username and valid password"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Navigate to login page
    login_page.navigate_to_login("https://ecommerce-website.com/login")
    
    # Enter empty username
    login_page.enter_email("")
    
    # Enter valid password
    login_page.enter_password_xpath("ValidPass123!")
    
    # Click login button
    login_page.click_login_xpath()
    
    # Get validation error
    error_visible = login_page.verify_login_failure()
    assert error_visible, "Validation error message not displayed for empty username"
    
    # Verify login prevented
    remain_on_login = login_page.verify_remain_on_login()
    assert remain_on_login, "User was not prevented from logging in with empty username"
    
    driver.quit()