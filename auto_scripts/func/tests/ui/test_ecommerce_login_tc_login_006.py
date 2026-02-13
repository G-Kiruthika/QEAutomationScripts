"""Test Case TC_LOGIN_006: Ecommerce Login Flow - Invalid Username"""

from core.driver_factory import get_driver
from pages.login_page import LoginPage


def test_login_invalid_username():
    """Test login failure with invalid username and valid password."""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Step 1: Navigate to login page
    login_page.navigate_to_login("https://ecommerce-website.com/login")
    # Expected: Login page is displayed
    
    # Step 2: Enter invalid username
    login_page.enter_invalid_username("invaliduser@example.com")
    # Expected: Invalid username is entered
    
    # Step 3: Enter valid password
    login_page.enter_valid_password("ValidPass123!")
    # Expected: Password is entered
    
    # Step 4: Click login button
    login_page.click_login()
    # Expected: Login fails with error message 'Invalid username or password'
    
    # Step 5: Verify user remains on login page
    on_login_page = login_page.verify_remain_on_login()
    # Expected: User is not authenticated and stays on login page
    assert on_login_page, "User should remain on login page after failed login"
    
    driver.quit()
