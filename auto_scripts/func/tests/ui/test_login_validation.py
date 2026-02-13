from core.driver_factory import get_driver
from pages.login_page import LoginPage
import pytest


def test_login_blank_username_validation():
    """
    Test Case TC_LOGIN_008: Verify login validation when username is blank
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Step 1: Navigate to login page
    login_page.navigate_to_login_page()
    
    # Step 2: Enter blank username
    login_page.enter_username('')
    
    # Step 3: Enter valid password
    login_page.enter_password('ValidPass123!')
    
    # Step 4: Click login button
    login_page.click_login_button()
    
    # Step 4: Verify validation error is displayed
    assert login_page.verify_validation_error(), "Validation error should be displayed for blank username"
    
    # Step 5: Verify login is prevented
    assert login_page.verify_login_prevented(), "Login should be prevented when username is blank"
    
    driver.quit()


def test_login_account_lockout_after_multiple_failed_attempts():
    """
    Test Case TC_LOGIN_010: Verify account lockout after 5 failed login attempts
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Step 1: Navigate to login page
    login_page.navigate_to_login_page()
    
    # Step 2: Enter valid username
    login_page.enter_username('validuser@example.com')
    
    # Step 3: Attempt login with wrong passwords (5 attempts)
    failed_passwords = ['WrongPass1', 'WrongPass2', 'WrongPass3', 'WrongPass4', 'WrongPass5']
    
    for wrong_password in failed_passwords:
        login_page.enter_password(wrong_password)
        login_page.click_login_button()
    
    # Step 4: Attempt with valid password after lockout
    login_page.enter_password('ValidPass123!')
    login_page.click_login_button()
    
    # Step 5: Verify account lockout message
    assert login_page.verify_account_lockout_message(), "Account lockout message should be displayed after 5 failed attempts"
    
    # Step 5: Verify email notification sent
    assert login_page.verify_email_notification_sent(), "Email notification should be sent about account lockout"
    
    driver.quit()
