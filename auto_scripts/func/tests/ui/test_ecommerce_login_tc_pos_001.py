"""Test Case TC-POS-001: Ecommerce Login Flow - Valid User Login"""

from core.driver_factory import get_driver
from pages.login_page import LoginPage


def test_login_valid_user():
    """Test successful login with valid credentials and session verification."""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Step 1: Navigate to login page
    login_page.navigate_to_login("https://ecommerce.example.com/login")
    # Expected: Login page is displayed with email and password fields
    
    # Step 2: Enter email
    login_page.enter_email("testuser@example.com")
    # Expected: Email is accepted and displayed in the field
    
    # Step 3: Enter password
    login_page.enter_password("Test@1234")
    # Expected: Password is masked and accepted
    
    # Step 4: Click login button
    login_page.click_login()
    # Expected: User is successfully authenticated and redirected to dashboard/home page
    
    # Step 5: Verify user session
    session_valid = login_page.verify_user_session()
    # Expected: User name is displayed in the header and session token is generated
    assert session_valid, "User session verification failed"
    
    driver.quit()
