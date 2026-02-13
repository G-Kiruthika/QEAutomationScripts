"""Test script for TC_LOGIN_010: Account Lockout After Multiple Failed Login Attempts"""

from pages.login_page import LoginPage
from core.driver_factory import get_driver
import time


def test_login_account_lockout():
    """Test case TC_LOGIN_010: Verify account lockout after 5 failed login attempts"""
    driver = get_driver()
    
    try:
        # Initialize page object
        login_page = LoginPage(driver)
        
        # Step 1: Navigate to login page
        login_page.navigate_to_login_page()
        
        # Step 2: Enter valid username
        login_page.enter_username("validuser@example.com")
        
        # Step 3: Attempt login with wrong passwords (5 attempts)
        failed_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
        
        for password in failed_passwords:
            login_page.enter_password(password)
            login_page.click_login_button()
            time.sleep(1)  # Small delay between attempts
        
        # Step 4: Attempt login with valid password after lockout
        login_page.enter_password("ValidPass123!")
        login_page.click_login_button()
        
        # Step 5: Verify account lockout message is displayed
        assert login_page.verify_account_lockout_message(), "Account lockout message should be displayed: 'Account locked due to multiple failed attempts. Please try again after 30 minutes or reset password'"
        
        # Step 5: Verify email notification was sent
        assert login_page.verify_email_notification_sent(), "Email notification should be sent to user about account lockout"
        
    finally:
        driver.quit()