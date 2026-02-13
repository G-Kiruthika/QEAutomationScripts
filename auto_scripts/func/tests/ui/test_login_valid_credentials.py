# test_login_valid_credentials.py
# Test Case ID: 501
# Feature: User Authentication
# Description: Validate login functionality with valid credentials

from core.driver_factory import get_driver
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_login_valid_credentials():
    """
    Test login functionality with valid user credentials.
    Validates complete authentication flow from login page to dashboard.
    """
    # Test data
    url = "https://ecommerce.example.com/login"
    email = "testuser@example.com"
    password = "Test@1234"
    
    # Initialize driver and page objects
    driver = get_driver()
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    
    try:
        # Step 1: Navigate to login page
        login_page.navigate_to_login_page(url)
        
        # Step 2: Verify login page is displayed
        assert login_page.is_login_page_displayed(), "Login page is not displayed"
        
        # Step 3: Enter email
        login_page.enter_email(email)
        
        # Step 4: Verify email is accepted
        assert login_page.is_email_accepted(), "Email was not accepted"
        
        # Step 5: Enter password
        login_page.enter_password(password)
        
        # Step 6: Verify password is accepted
        assert login_page.is_password_accepted(), "Password was not accepted"
        
        # Step 7: Click login button
        login_page.click_login_button()
        
        # Step 8: Verify user is authenticated
        assert login_page.is_user_authenticated(), "User authentication failed"
        
        # Step 9: Verify dashboard is displayed
        assert dashboard_page.is_dashboard_displayed(), "Dashboard is not displayed after login"
        
        # Step 10: Verify user session
        dashboard_page.verify_user_session()
        
        # Step 11: Verify user header is displayed
        assert dashboard_page.is_user_header_displayed(), "User header is not displayed on dashboard"
        
        # Step 12: Verify session token is generated
        assert login_page.is_session_token_generated(), "Session token was not generated"
        
    finally:
        driver.quit()
