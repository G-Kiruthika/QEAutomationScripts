from pages.login_page import LoginPage
from core.driver_factory import get_driver

def test_login_blank_username():
    """Test Case TC_LOGIN_008: Login with blank username"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Step 1: Navigate to login page
    login_page.navigate_to_login("https://ecommerce-website.com/login")
    
    # Step 2: Enter blank username
    login_page.enter_username("")
    
    # Step 3: Enter valid password
    login_page.enter_password("ValidPass123!")
    
    # Step 4: Click login button
    login_page.click_login()
    
    # Step 5: Verify validation error is displayed
    assert login_page.is_validation_error_displayed(), "Validation error should be displayed"
    error_message = login_page.get_validation_error()
    assert error_message == "Username is required", f"Expected 'Username is required', got '{error_message}'"
    
    driver.quit()
