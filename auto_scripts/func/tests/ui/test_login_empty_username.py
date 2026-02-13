from core.driver_factory import get_driver
from pages.login_page import LoginPage

def test_login_empty_username():
    """Test login with empty username field"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Navigate to login page
    login_page.navigate_to_login_page("https://ecommerce-website.com/login")
    
    # Enter empty username
    login_page.enter_username("")
    
    # Enter valid password
    login_page.enter_password("ValidPass123!")
    
    # Click login button
    login_page.click_login_button()
    
    # Assert validation error message
    error_message = login_page.get_validation_error_message()
    assert error_message == "Username is required", f"Expected 'Username is required', but got '{error_message}'"
    
    # Assert user remains on login page (verify login not submitted)
    current_url = driver.current_url
    assert "login" in current_url.lower(), f"User should remain on login page, but current URL is {current_url}"
    
    driver.quit()
