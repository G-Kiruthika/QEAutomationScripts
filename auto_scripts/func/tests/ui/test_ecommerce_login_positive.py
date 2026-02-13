# Test Case TC-POS-001: Positive Login Flow
from core.driver_factory import get_driver
from pages.login_page import LoginPage

def test_login_valid_user():
    """Test Case TC-POS-001: Verify successful login with valid credentials."""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Step 1: Navigate to login page
    login_page.navigate_to_login('https://ecommerce.example.com/login')
    
    # Step 2: Enter email
    login_page.enter_email('testuser@example.com')
    
    # Step 3: Enter password
    login_page.enter_password_xpath('Test@1234')
    
    # Step 4: Click login button
    login_page.click_login_xpath()
    
    # Step 5: Verify user session and successful login
    assert login_page.verify_login_success(), "Login page dashboard not visible"
    assert login_page.verify_user_session(), "User session not created"
    
    driver.quit()
