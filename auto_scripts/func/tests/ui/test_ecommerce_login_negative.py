# Test Case TC_LOGIN_006: Negative Login Flow with Invalid Username
from core.driver_factory import get_driver
from pages.login_page import LoginPage

def test_login_invalid_username():
    """Test Case TC_LOGIN_006: Verify login fails with invalid username."""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Step 1: Navigate to login page
    login_page.navigate_to_login('https://ecommerce-website.com/login')
    
    # Step 2: Enter invalid username
    login_page.enter_invalid_username('invaliduser@example.com')
    
    # Step 3: Enter valid password
    login_page.enter_valid_password('ValidPass123!')
    
    # Step 4: Click login button
    login_page.click_login_xpath()
    
    # Step 5: Verify login failure and user remains on login page
    assert login_page.verify_login_failure(), "Error message not displayed"
    assert login_page.verify_remain_on_login(), "User not on login page"
    
    driver.quit()
