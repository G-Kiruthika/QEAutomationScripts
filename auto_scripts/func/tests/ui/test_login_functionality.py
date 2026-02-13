"""Login Functionality Test Suite

This module contains automated test cases for login functionality
including validation, authentication, and account lockout scenarios.
"""

import pytest
from core.driver_factory import get_driver
from pages.login_page import LoginPage


def test_login_blank_username_validation():
    """Test Case TC_LOGIN_008: Verify validation error when username is blank.
    
    This test verifies that the system displays appropriate validation error
    when user attempts to login with blank username and valid password.
    
    Test Steps:
    1. Navigate to login page
    2. Leave username field blank
    3. Enter valid password
    4. Click login button
    5. Verify validation error is displayed
    6. Verify login is prevented
    
    Expected Result:
    - Validation error message displayed: 'Username is required'
    - Login request is not submitted
    - User remains on login page
    """
    driver = get_driver()
    try:
        login_page = LoginPage(driver)
        
        # Step 1: Navigate to login page
        login_page.navigate_to_login_page()
        
        # Step 2: Leave username field blank (enter empty string)
        login_page.enter_username("")
        
        # Step 3: Enter valid password
        login_page.enter_password("ValidPass123!")
        
        # Step 4: Click login button
        login_page.click_login_button()
        
        # Step 5: Verify validation error is displayed
        assert login_page.verify_validation_error(), "Validation error message should be displayed for blank username"
        
        # Step 6: Verify login is prevented
        assert login_page.verify_login_prevented(), "Login should be prevented when username is blank"
        
    finally:
        driver.quit()


def test_account_lockout_after_multiple_failed_attempts():
    """Test Case TC_LOGIN_010: Verify account lockout after 5 failed login attempts.
    
    This test verifies that the system locks the account after 5 consecutive
    failed login attempts and sends email notification to the user.
    
    Test Steps:
    1. Navigate to login page
    2. Enter valid username
    3. Attempt login with 5 different wrong passwords
    4. Attempt login with correct password after lockout
    5. Verify account lockout message is displayed
    6. Verify email notification is sent
    
    Expected Result:
    - Account is locked after 5 failed attempts
    - Error message displayed: 'Account locked due to multiple failed attempts. Please try again after 30 minutes or reset password'
    - Email notification sent to user about account lockout
    - Login is prevented even with correct password
    """
    driver = get_driver()
    try:
        login_page = LoginPage(driver)
        
        # Step 1: Navigate to login page
        login_page.navigate_to_login_page()
        
        # Step 2: Enter valid username
        login_page.enter_username("validuser@example.com")
        
        # Step 3: Attempt login with 5 different wrong passwords
        wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
        
        for wrong_password in wrong_passwords:
            login_page.enter_password(wrong_password)
            login_page.click_login_button()
            # After each failed attempt, re-enter username for next attempt
            if wrong_password != wrong_passwords[-1]:  # Not the last attempt
                login_page.enter_username("validuser@example.com")
        
        # Step 4: Attempt login with correct password after lockout
        login_page.enter_password("ValidPass123!")
        login_page.click_login_button()
        
        # Step 5: Verify account lockout message is displayed
        assert login_page.verify_account_lockout_message(), "Account lockout message should be displayed after 5 failed attempts"
        
        # Step 6: Verify email notification is sent
        assert login_page.verify_email_notification_sent(), "Email notification should be sent to user about account lockout"
        
    finally:
        driver.quit()