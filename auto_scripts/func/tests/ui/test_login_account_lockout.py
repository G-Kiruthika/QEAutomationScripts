from core.driver_factory import get_driver
from pages.login_page import LoginPage

def test_login_account_lockout_after_failed_attempts():
    """Test account lockout after multiple failed login attempts"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Navigate to login page
    login_page.navigate_to_login_page("https://ecommerce-website.com/login")
    
    # Enter valid username
    login_page.enter_username("validuser@example.com")
    
    # First failed attempt
    login_page.enter_password("WrongPass1")
    login_page.click_login_button()
    
    # Assert error message after first attempt
    error_message = login_page.get_validation_error_message()
    assert error_message != "", "Error message should be displayed after failed login"
    
    # Repeat failed attempts with different wrong passwords
    wrong_passwords = ["WrongPass2", "WrongPass3", "WrongPass4", "WrongPass5"]
    for wrong_password in wrong_passwords:
        login_page.enter_password(wrong_password)
        login_page.click_login_button()
    
    # Attempt login with correct password after multiple failures
    login_page.enter_password("ValidPass123!")
    login_page.click_login_button()
    
    # Assert account lockout message
    lockout_message = login_page.get_account_lockout_message()
    expected_lockout_msg = "Account locked due to multiple failed attempts. Please try again after 30 minutes or reset password"
    assert expected_lockout_msg in lockout_message or lockout_message != "", f"Expected account lockout message, but got '{lockout_message}'"
    
    # Assert email notification sent
    email_notification_visible = login_page.verify_email_notification_sent()
    assert email_notification_visible, "Email notification should be sent to user about account lockout"
    
    driver.quit()
