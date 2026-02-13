from pages.login_page import LoginPage
from core.driver_factory import get_driver
import pytest


def test_login_validation_tc_login_008():
    """Test case to verify validation error when username is left empty"""
    driver = get_driver()
    try:
        login_page = LoginPage(driver)
        
        # Navigate to login page
        login_page.navigate_to_login_page("https://ecommerce-website.com/login")
        
        # Leave username empty and enter valid password
        login_page.enter_username("")
        login_page.enter_password("ValidPass123!")
        
        # Click login button
        login_page.click_login()
        
        # Verify validation error is displayed
        validation_error = login_page.get_validation_error_message()
        assert validation_error is not None, "Validation error message should be displayed"
        
        # Verify login is prevented (error message should be visible)
        assert login_page.is_error_message_displayed(), "Login should be prevented when username is empty"
        
    finally:
        driver.quit()


def test_account_lockout_tc_login_010():
    """Test case to verify account lockout after multiple failed login attempts"""
    driver = get_driver()
    try:
        login_page = LoginPage(driver)
        
        # Navigate to login page
        login_page.navigate_to_login_page("https://ecommerce-website.com/login")
        
        # Test data
        username = "validuser@example.com"
        passwords = [
            "WrongPass1",
            "WrongPass2",
            "WrongPass3",
            "WrongPass4",
            "WrongPass5",
            "ValidPass123!"
        ]
        
        # Attempt login with wrong passwords (first 5 attempts)
        for i in range(5):
            login_page.enter_username(username)
            login_page.enter_password(passwords[i])
            login_page.click_login()
        
        # Attempt login with correct password (6th attempt)
        login_page.enter_username(username)
        login_page.enter_password(passwords[5])
        login_page.click_login()
        
        # Verify account lockout notification
        lockout_message = login_page.get_account_lockout_message()
        assert lockout_message is not None, "Account lockout message should be displayed after multiple failed attempts"
        
        # Verify email notification was sent
        assert login_page.verify_email_notification_sent(), "Email notification should be sent for account lockout"
        
    finally:
        driver.quit()
