# tests/ui/test_login_functionality.py

from pages.login_page import LoginPage
from core.driver_factory import get_driver
import pytest


def test_tc_login_008_blank_username_validation():
    """
    Test Case TC_LOGIN_008: Verify login is prevented when username is blank
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Step 1: Navigate to login page
    login_page.navigate_to("https://ecommerce-website.com/login")
    
    # Step 2: Enter blank username
    login_page.enter_username("")
    
    # Step 3: Enter password
    login_page.enter_password("ValidPass123!")
    
    # Step 4: Click login button
    login_page.click_login_button()
    
    # Step 5: Verify login is prevented and validation error is displayed
    assert login_page.is_validation_error_displayed(), "Validation error should be displayed"
    assert "Username is required" in login_page.get_error_message(), "Error message should indicate username is required"
    assert login_page.is_on_login_page(), "User should remain on login page"
    
    driver.quit()


def test_tc_login_010_account_lockout_after_multiple_failed_attempts():
    """
    Test Case TC_LOGIN_010: Verify account lockout after 5 failed login attempts
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Step 1: Navigate to login page
    login_page.navigate_to("https://ecommerce-website.com/login")
    
    # Step 2: Enter valid username
    login_page.enter_username("validuser@example.com")
    
    # Step 3: Attempt login with wrong passwords 5 times
    wrong_passwords = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
    
    for password in wrong_passwords:
        login_page.enter_password(password)
        login_page.click_login_button()
        # Verify each attempt fails
        assert login_page.is_error_message_displayed(), f"Error message should be displayed for attempt with {password}"
    
    # Step 4: Try with valid password after 5 failed attempts
    login_page.enter_password("ValidPass123!")
    login_page.click_login_button()
    
    # Step 5: Verify account lockout message
    assert login_page.is_account_locked_message_displayed(), "Account locked message should be displayed"
    lockout_message = login_page.get_lockout_message()
    assert "Account locked due to multiple failed attempts" in lockout_message, "Lockout message should indicate account is locked"
    assert "Please try again after 30 minutes or reset password" in lockout_message, "Lockout message should provide recovery options"
    
    # Verify email notification was sent (this would typically be verified through email service or logs)
    # For now, we verify the UI indicates notification was sent
    assert login_page.is_email_notification_indicated(), "Email notification should be indicated"
    
    driver.quit()
