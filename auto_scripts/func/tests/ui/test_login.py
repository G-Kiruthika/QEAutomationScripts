from core.driver_factory import get_driver
from pages.login_page import LoginPage
import pytest


def test_tc_pos_001_valid_login():
    """Test case for valid login functionality"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Test data
    url = 'https://ecommerce.example.com/login'
    email = 'testuser@example.com'
    password = 'Test@1234'
    
    try:
        # Execute test flow
        login_page.navigate_to_login_page(url)
        login_page.enter_email(email)
        login_page.enter_password(password)
        login_page.click_login_button()
        
        # Assertions
        assert login_page.is_user_authenticated(), "User authentication failed"
        assert login_page.is_user_name_displayed(), "User name is not displayed"
        assert login_page.is_session_token_generated(), "Session token was not generated"
    finally:
        driver.quit()


def test_tc_login_006_invalid_login():
    """Test case for invalid login functionality"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Test data
    url = 'https://ecommerce-website.com/login'
    username = 'invaliduser@example.com'
    password = 'ValidPass123!'
    
    try:
        # Execute test flow
        login_page.navigate_to_login_page(url)
        login_page.enter_email(username)
        login_page.enter_password(password)
        login_page.click_login_button()
        
        # Assertions
        assert login_page.is_error_message_displayed(), "Error message is not displayed"
        assert login_page.is_on_login_page(), "User is not on login page"
    finally:
        driver.quit()
