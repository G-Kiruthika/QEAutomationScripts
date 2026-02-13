# tests/ui/test_login.py
# Functional UI Test Suite for Login Feature

from core.driver_factory import get_driver
from pages.login_page import LoginPage


def test_login_username_empty():
    """
    Test Case ID: 508
    Feature: Login
    Scenario: Verify error message when username field is empty
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Test data
    url = "https://ecommerce-website.com/login"
    username = ""
    password = "ValidPass123!"
    expected_message = "Username is required"
    
    try:
        # Test flow
        login_page.navigate_to_login_page(url)
        login_page.leave_username_empty()
        login_page.enter_password(password)
        login_page.click_login()
        
        # Assertions
        login_page.verify_error_message(expected_message)
        login_page.verify_login_prevented()
    finally:
        driver.quit()


def test_login_account_lockout():
    """
    Test Case ID: 510
    Feature: Login
    Scenario: Verify account lockout after multiple failed login attempts
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Test data
    url = "https://ecommerce-website.com/login"
    username = "validuser@example.com"
    wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
    valid_password = "ValidPass123!"
    invalid_cred_message = "Invalid credentials"
    account_locked_message = "Account locked due to multiple failed attempts. Please try again after 30 minutes or reset password"
    
    try:
        # Test flow
        login_page.navigate_to_login_page(url)
        login_page.enter_username(username)
        
        # Attempt login with wrong passwords multiple times
        for wrong_password in wrong_passwords:
            login_page.enter_password(wrong_password)
            login_page.click_login()
            login_page.verify_error_message(invalid_cred_message)
        
        # Attempt login with valid password after lockout
        login_page.enter_password(valid_password)
        login_page.click_login()
        
        # Assertions
        login_page.verify_error_message(account_locked_message)
        login_page.verify_account_lockout_notification()
    finally:
        driver.quit()