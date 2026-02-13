"""Login validation test suite.

This module contains test cases for login functionality validation including
valid credentials, invalid credentials, account lockout, and email notifications.
"""

from core.driver_factory import get_driver
from pages.login_page import LoginPage


def test_login_with_valid_credentials():
    """
    Test login functionality with valid username and password.
    
    Steps:
    1. Navigate to login page
    2. Enter valid username
    3. Enter valid password
    4. Click login button
    5. Verify successful login
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    login_page.navigate_to_login_page()
    login_page.enter_username("testuser@example.com")
    login_page.enter_password("SecurePass123")
    login_page.click_login_button()
    
    # Assertion: Verify login success (implementation depends on success indicator)
    assert driver.current_url != "/login", "Login failed - still on login page"
    
    driver.quit()


def test_login_with_invalid_credentials():
    """
    Test login functionality with invalid username and password.
    
    Steps:
    1. Navigate to login page
    2. Enter invalid username
    3. Enter invalid password
    4. Click login button
    5. Verify validation error message is displayed
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    login_page.navigate_to_login_page()
    login_page.enter_username("invaliduser@example.com")
    login_page.enter_password("WrongPass456")
    login_page.click_login_button()
    
    error_message = login_page.get_validation_error_message()
    
    # Assertion: Verify error message is displayed
    assert error_message is not None, "Validation error message not displayed"
    assert "invalid" in error_message.lower() or "incorrect" in error_message.lower(), \n        f"Unexpected error message: {error_message}"
    
    driver.quit()


def test_account_lockout_after_multiple_failed_attempts():
    """
    Test account lockout mechanism after multiple failed login attempts.
    
    Steps:
    1. Navigate to login page
    2. Attempt login with invalid credentials (attempt 1)
    3. Attempt login with invalid credentials (attempt 2)
    4. Attempt login with invalid credentials (attempt 3)
    5. Verify account lockout message is displayed
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    login_page.navigate_to_login_page()
    
    # Attempt 1
    login_page.enter_username("testuser@example.com")
    login_page.enter_password("WrongPass1")
    login_page.click_login_button()
    
    # Attempt 2
    login_page.enter_username("testuser@example.com")
    login_page.enter_password("WrongPass2")
    login_page.click_login_button()
    
    # Attempt 3
    login_page.enter_username("testuser@example.com")
    login_page.enter_password("WrongPass3")
    login_page.click_login_button()
    
    lockout_message = login_page.get_account_lockout_message()
    
    # Assertion: Verify account lockout message is displayed
    assert lockout_message is not None, "Account lockout message not displayed"
    assert "locked" in lockout_message.lower() or "blocked" in lockout_message.lower(), \n        f"Unexpected lockout message: {lockout_message}"
    
    driver.quit()


def test_email_notification_on_successful_login():
    """
    Test email notification is sent upon successful login.
    
    Steps:
    1. Navigate to login page
    2. Enter valid username
    3. Enter valid password
    4. Click login button
    5. Verify email notification was sent
    """
    driver = get_driver()
    login_page = LoginPage(driver)
    
    login_page.navigate_to_login_page()
    login_page.enter_username("testuser@example.com")
    login_page.enter_password("SecurePass123")
    login_page.click_login_button()
    
    email_sent = login_page.verify_email_notification_sent()
    
    # Assertion: Verify email notification element is present
    assert email_sent is True, "Email notification was not sent after successful login"
    
    driver.quit()