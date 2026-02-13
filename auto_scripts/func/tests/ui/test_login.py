# tests/ui/test_login.py

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from core.driver_factory import get_driver


def test_login_valid_credentials():
    """Test login functionality with valid credentials"""
    driver = get_driver()
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    
    # Navigate to login page
    login_page.open()
    
    # Perform login with valid credentials
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login_button()
    
    # Verify successful login
    assert dashboard_page.is_dashboard_visible(), "Dashboard should be visible after successful login"
    assert dashboard_page.get_welcome_message() == "Welcome, standard_user", "Welcome message should match expected text"
    
    driver.quit()


def test_login_invalid_username():
    """Test login functionality with invalid username"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Navigate to login page
    login_page.open()
    
    # Attempt login with invalid username
    login_page.enter_username("invalid_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login_button()
    
    # Verify error message is displayed
    assert login_page.is_error_message_visible(), "Error message should be visible for invalid credentials"
    assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service", "Error message should match expected text"
    
    driver.quit()
