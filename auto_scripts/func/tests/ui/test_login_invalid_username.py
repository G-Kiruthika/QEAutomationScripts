from pages.login_page import LoginPage
from core.driver_factory import get_driver

def test_login_invalid_username():
    """Test login with invalid username and verify error message"""
    driver = get_driver()
    
    # Initialize page object
    login_page = LoginPage(driver)
    
    # Test data
    url = "https://ecommerce-website.com/login"
    email = "invaliduser@example.com"
    password = "ValidPass123!"
    error_message = "Invalid username or password"
    
    # Test flow
    login_page.navigate_to_login_page(url)
    assert login_page.is_login_page_displayed(), "Login page should be displayed"
    
    login_page.enter_email(email)
    assert login_page.is_email_accepted(), "Email should be accepted"
    
    login_page.enter_password(password)
    assert login_page.is_password_accepted(), "Password should be accepted"
    
    login_page.click_login_button()
    assert login_page.is_error_message_displayed(), "Error message should be displayed"
    
    assert login_page.is_still_on_login_page(), "Should still be on login page"
    
    driver.quit()
