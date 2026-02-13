# tests/ui/test_login.py

from pages.login_page import LoginPage
from core.driver_factory import get_driver


def test_login_username_empty():
    """
    Test Case ID: 508
    Feature: Login
    Scenario: Verify login fails when username is empty
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Navigate to login page
    login_page.navigate_to_login_page("https://ecommerce-website.com/login")
    
    # Leave username empty
    login_page.leave_username_empty("")
    
    # Enter password
    login_page.enter_password("ValidPass123!")
    
    # Click login button
    login_page.click_login()
    
    # Verify error message
    assert login_page.verify_error_message("Username is required"), "Expected error message 'Username is required' not displayed"
    
    # Verify login is prevented
    assert login_page.verify_login_prevented(), "Login should be prevented when username is empty"
    
    driver.quit()


def test_login_account_lockout():
    """
    Test Case ID: 510
    Feature: Login
    Scenario: Verify account lockout after multiple failed login attempts
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Navigate to login page
    login_page.navigate_to_login_page("https://ecommerce-website.com/login")
    
    # Enter username
    login_page.enter_username("validuser@example.com")
    
    # Attempt login with wrong passwords multiple times
    wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
    for wrong_pass in wrong_passwords:
        login_page.enter_password(wrong_pass)
        login_page.click_login()
        assert login_page.verify_error_message("Invalid credentials"), "Expected 'Invalid credentials' error message"
    
    # Attempt login with valid password after lockout
    login_page.enter_password("ValidPass123!")
    login_page.click_login()
    
    # Verify account locked message
    assert login_page.verify_error_message("Account locked due to multiple failed attempts. Please try again after 30 minutes or reset password"), "Expected account lockout message not displayed"
    
    # Verify account lockout notification
    assert login_page.verify_account_lockout_notification(), "Account lockout notification not displayed"
    
    driver.quit()