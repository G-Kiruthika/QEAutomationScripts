"""Login Test Suite

This module contains functional tests for the Login feature.
Follows Python UI & API Automation Framework Reference Document standards.
"""

from core.driver_factory import get_driver
from pages.login_page import LoginPage
import pytest


def test_tc_pos_001():
    """Test Case: TC_POS_001 - Valid User Login
    
    Validates successful login with valid credentials.
    """
    driver = get_driver()
    try:
        login_page = LoginPage(driver)
        
        # Navigate to login page
        login_page.navigate_to_login_page("https://ecommerce.example.com/login")
        
        # Validate login page is displayed
        assert login_page.validate_login_page_displayed(), "Login page should be displayed"
        
        # Enter email
        login_page.enter_email("testuser@example.com")
        
        # Enter password
        login_page.enter_password("Test@1234")
        
        # Click login button
        login_page.click_login_button()
        
        # Validate user is authenticated
        assert login_page.validate_user_authenticated(), "User should be authenticated after login"
        
        # Validate user is authenticated (duplicate assertion as per flow)
        assert login_page.validate_user_authenticated(), "User authentication should persist"
        
    finally:
        driver.quit()


def test_tc_login_006():
    """Test Case: TC_LOGIN_006 - Invalid User Login
    
    Validates login failure with invalid credentials and proper error handling.
    """
    driver = get_driver()
    try:
        login_page = LoginPage(driver)
        
        # Navigate to login page
        login_page.navigate_to_login_page("https://ecommerce-website.com/login")
        
        # Enter invalid email
        login_page.enter_email("invaliduser@example.com")
        
        # Enter password
        login_page.enter_password("ValidPass123!")
        
        # Click login button
        login_page.click_login_button()
        
        # Validate error message is displayed
        assert login_page.validate_error_message_displayed(), "Error message should be displayed for invalid credentials"
        
        # Validate user is not authenticated
        assert login_page.validate_user_not_authenticated(), "User should not be authenticated with invalid credentials"
        
    finally:
        driver.quit()
