"""Test script for TC_LOGIN_008: Blank Username Field Validation"""

from pages.login_page import LoginPage
from core.driver_factory import get_driver


def test_login_blank_username():
    """Test case TC_LOGIN_008: Verify validation error when username field is blank"""
    driver = get_driver()
    
    try:
        # Initialize page object
        login_page = LoginPage(driver)
        
        # Step 1: Navigate to login page
        login_page.navigate_to_login_page()
        
        # Step 2: Enter blank username
        login_page.enter_username("")
        
        # Step 3: Enter valid password
        login_page.enter_password("ValidPass123!")
        
        # Step 4: Click login button and verify validation error
        login_page.click_login_button()
        assert login_page.verify_validation_error(), "Validation error 'Username is required' should be displayed"
        
        # Step 5: Verify login is prevented
        assert login_page.verify_login_prevented(), "Login request should not be submitted, user should remain on login page"
        
    finally:
        driver.quit()