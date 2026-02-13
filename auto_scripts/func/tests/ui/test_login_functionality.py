# tests/ui/test_login_functionality.py

from pages.login_page import LoginPage
from core.driver_factory import get_driver
import yaml

def test_login_valid_user():
    """Test login with valid credentials"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Load test data from config
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    username = config['test_data']['valid_user']['username']
    password = config['test_data']['valid_user']['password']
    
    login_page.open()
    login_page.login(username, password)
    
    # Assertion
    assert login_page.is_logged_in(), "User should be logged in successfully"
    
    driver.quit()

def test_login_invalid_user():
    """Test login with invalid credentials"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    # Load test data from config
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    username = config['test_data']['invalid_user']['username']
    password = config['test_data']['invalid_user']['password']
    
    login_page.open()
    login_page.login(username, password)
    
    # Assertion
    assert login_page.is_error_displayed(), "Error message should be displayed for invalid credentials"
    
    driver.quit()

def test_login_empty_credentials():
    """Test login with empty credentials"""
    driver = get_driver()
    login_page = LoginPage(driver)
    
    login_page.open()
    login_page.login("", "")
    
    # Assertion
    assert login_page.is_error_displayed(), "Error message should be displayed for empty credentials"
    
    driver.quit()
