from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from core.driver_factory import get_driver

def test_login_valid_credentials():
    """Test login with valid credentials and verify dashboard access"""
    driver = get_driver()
    
    # Initialize page objects
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    
    # Test data
    url = "https://ecommerce.example.com/login"
    email = "testuser@example.com"
    password = "Test@1234"
    
    # Test flow
    login_page.navigate_to_login_page(url)
    assert login_page.is_login_page_displayed(), "Login page should be displayed"
    
    login_page.enter_email(email)
    assert login_page.is_email_accepted(), "Email should be accepted"
    
    login_page.enter_password(password)
    assert login_page.is_password_accepted(), "Password should be accepted"
    
    login_page.click_login_button()
    assert login_page.is_user_authenticated(), "User should be authenticated"
    
    assert dashboard_page.is_dashboard_displayed(), "Dashboard should be displayed"
    
    dashboard_page.verify_user_session()
    assert dashboard_page.is_user_header_displayed(), "User header should be displayed"
    
    assert login_page.is_session_token_generated(), "Session token should be generated"
    
    driver.quit()
