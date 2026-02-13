# test_login_invalid_username.py
# Test Case ID: 504
# Feature: User Authentication
# Description: Validate login error handling with invalid username

from core.driver_factory import get_driver
from pages.login_page import LoginPage


def test_login_invalid_username():
    """
    Test login functionality with invalid username.
    Validates error message display and user remains on login page.
    """
    # Test data
    url = "https://ecommerce-website.com/login"
    email = "invaliduser@example.com"
    password = "ValidPass123!"
    error_message = "Invalid username or password"
    
    # Initialize driver and page objects
    driver = get_driver()
    login_page = LoginPage(driver)
    
    try:
        # Step 1: Navigate to login page
        login_page.navigate_to_login_page(url)
        
        # Step 2: Verify login page is displayed
        assert login_page.is_login_page_displayed(), "Login page is not displayed"
        
        # Step 3: Enter invalid email
        login_page.enter_email(email)
        
        # Step 4: Verify email is accepted (field accepts input)
        assert login_page.is_email_accepted(), "Email field did not accept input"
        
        # Step 5: Enter password
        login_page.enter_password(password)
        
        # Step 6: Verify password is accepted (field accepts input)
        assert login_page.is_password_accepted(), "Password field did not accept input"
        
        # Step 7: Click login button
        login_page.click_login_button()
        
        # Step 8: Verify error message is displayed
        assert login_page.is_error_message_displayed(), "Error message is not displayed for invalid credentials"
        
        # Step 9: Verify user is still on login page
        assert login_page.is_still_on_login_page(), "User was redirected despite invalid credentials"
        
    finally:
        driver.quit()
