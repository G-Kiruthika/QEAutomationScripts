from pages.login_page import LoginPage
from core.driver_factory import get_driver

def test_login_account_lockout():
    """Test Case TC_LOGIN_010: Account lockout after multiple failed login attempts"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Step 1: Navigate to login page
    login_page.navigate_to_login("https://ecommerce-website.com/login")
    
    # Step 2: Enter valid username
    login_page.enter_username("validuser@example.com")
    
    # Step 3: Attempt login with wrong passwords 5 times
    password_attempts = ["WrongPass1", "WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
    
    for attempt_password in password_attempts:
        login_page.enter_password(attempt_password)
        login_page.click_login()
        assert login_page.is_error_message_displayed(), f"Error message should be displayed for failed attempt with {attempt_password}"
    
    # Step 4: Enter valid password after account is locked
    login_page.enter_password("ValidPass123!")
    login_page.click_login()
    
    # Verify account lockout message
    assert login_page.is_error_message_displayed(), "Account lockout error should be displayed"
    lockout_message = login_page.get_error_message()
    expected_lockout_message = "Account locked due to multiple failed attempts. Please try again after 30 minutes or reset password"
    assert expected_lockout_message in lockout_message, f"Expected lockout message, got '{lockout_message}'"
    
    # Step 5: Verify account lockout notification
    assert login_page.verify_account_lockout_notification(), "Account lockout notification should be visible"
    
    driver.quit()
