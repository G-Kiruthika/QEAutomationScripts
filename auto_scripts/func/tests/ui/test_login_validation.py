from core.driver_factory import get_driver
from pages.login_page import LoginPage
import pytest
import yaml


def test_login_empty_username():
    """TC_LOGIN_008: Test login with empty username field"""
    # Load configuration
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    # Initialize driver and page object
    driver = get_driver()
    login_page = LoginPage(driver)
    
    try:
        # Navigate to login page
        driver.get(config['test_data']['TC_LOGIN_008']['url'])
        
        # Enter empty username
        login_page.enter_username(config['test_data']['TC_LOGIN_008']['username'])
        
        # Enter valid password
        login_page.enter_password(config['test_data']['TC_LOGIN_008']['password'])
        
        # Click login button
        login_page.click_login()
        
        # Verify validation error is displayed
        assert login_page.is_error_message_displayed(), "Validation error should be displayed for empty username"
        
        # Verify login is prevented (login button should still be visible)
        assert login_page.is_login_button_enabled(), "Login should be prevented with empty username"
        
    finally:
        driver.quit()


def test_login_account_lockout():
    """TC_LOGIN_010: Test account lockout after multiple failed login attempts"""
    # Load configuration
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    # Initialize driver and page object
    driver = get_driver()
    login_page = LoginPage(driver)
    
    try:
        # Navigate to login page
        driver.get(config['test_data']['TC_LOGIN_010']['url'])
        
        # Enter username
        username = config['test_data']['TC_LOGIN_010']['username']
        login_page.enter_username(username)
        
        # Attempt login with incorrect passwords (5 times)
        incorrect_passwords = config['test_data']['TC_LOGIN_010']['incorrect_passwords']
        for wrong_password in incorrect_passwords:
            login_page.enter_password(wrong_password)
            login_page.click_login()
        
        # Attempt login with correct password (should be locked out)
        login_page.enter_password(config['test_data']['TC_LOGIN_010']['correct_password'])
        login_page.click_login()
        
        # Verify account lockout message is displayed
        assert login_page.is_error_message_displayed(), "Account lockout message should be displayed"
        
        # Verify email notification was sent (this would typically be verified via email service or mock)
        # For now, we assert the error message is present as indication of lockout
        from utils.email_notification_handler import verify_lockout_email_sent
        assert verify_lockout_email_sent(username), "Email notification should be sent for account lockout"
        
    finally:
        driver.quit()