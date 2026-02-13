# tests/ui/test_user_registration.py

from pages.registration_page import RegistrationPage
from core.driver_factory import get_driver
import yaml

def test_registration_valid_user():
    """Test successful user registration with valid data"""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    # Load test data from config
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    test_data = config['test_data']['registration']['valid_user']
    
    registration_page.open()
    registration_page.enter_username(test_data['username'])
    registration_page.enter_email(test_data['email'])
    registration_page.enter_password(test_data['password'])
    registration_page.enter_confirm_password(test_data['password'])
    registration_page.click_register_button()
    
    # Assertion
    assert registration_page.is_registration_successful(), "Registration should be successful with valid data"
    driver.quit()

def test_registration_invalid_email():
    """Test registration with invalid email format"""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    test_data = config['test_data']['registration']['invalid_email']
    
    registration_page.open()
    registration_page.enter_username(test_data['username'])
    registration_page.enter_email(test_data['email'])
    registration_page.enter_password(test_data['password'])
    registration_page.enter_confirm_password(test_data['password'])
    registration_page.click_register_button()
    
    # Assertion
    assert registration_page.is_error_message_displayed(), "Error message should be displayed for invalid email"
    assert "invalid email" in registration_page.get_error_message().lower(), "Error message should mention invalid email"
    driver.quit()

def test_registration_password_mismatch():
    """Test registration with mismatched passwords"""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    test_data = config['test_data']['registration']['password_mismatch']
    
    registration_page.open()
    registration_page.enter_username(test_data['username'])
    registration_page.enter_email(test_data['email'])
    registration_page.enter_password(test_data['password'])
    registration_page.enter_confirm_password(test_data['confirm_password'])
    registration_page.click_register_button()
    
    # Assertion
    assert registration_page.is_error_message_displayed(), "Error message should be displayed for password mismatch"
    assert "password" in registration_page.get_error_message().lower(), "Error message should mention password mismatch"
    driver.quit()

def test_registration_empty_fields():
    """Test registration with empty required fields"""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    registration_page.open()
    registration_page.click_register_button()
    
    # Assertion
    assert registration_page.is_error_message_displayed(), "Error message should be displayed for empty fields"
    driver.quit()

def test_registration_duplicate_username():
    """Test registration with already existing username"""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    test_data = config['test_data']['registration']['duplicate_username']
    
    registration_page.open()
    registration_page.enter_username(test_data['username'])
    registration_page.enter_email(test_data['email'])
    registration_page.enter_password(test_data['password'])
    registration_page.enter_confirm_password(test_data['password'])
    registration_page.click_register_button()
    
    # Assertion
    assert registration_page.is_error_message_displayed(), "Error message should be displayed for duplicate username"
    assert "already exists" in registration_page.get_error_message().lower() or "taken" in registration_page.get_error_message().lower(), "Error message should mention username already exists"
    driver.quit()