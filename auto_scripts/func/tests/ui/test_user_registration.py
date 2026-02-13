# tests/ui/test_user_registration.py

from pages.registration_page import RegistrationPage
from core.driver_factory import get_driver
import yaml


def test_valid_user_registration():
    """Test successful user registration with valid data"""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    # Load test data from config
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    test_data = config['test_data']['registration']['valid_user']
    
    try:
        registration_page.open()
        registration_page.enter_username(test_data['username'])
        registration_page.enter_email(test_data['email'])
        registration_page.enter_password(test_data['password'])
        registration_page.enter_confirm_password(test_data['password'])
        registration_page.click_register_button()
        
        # Assertion
        assert registration_page.is_registration_successful(), "Registration should be successful"
        
    finally:
        driver.quit()


def test_registration_with_existing_email():
    """Test registration with an already registered email"""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    # Load test data from config
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    test_data = config['test_data']['registration']['existing_email']
    
    try:
        registration_page.open()
        registration_page.enter_username(test_data['username'])
        registration_page.enter_email(test_data['email'])
        registration_page.enter_password(test_data['password'])
        registration_page.enter_confirm_password(test_data['password'])
        registration_page.click_register_button()
        
        # Assertion
        error_message = registration_page.get_error_message()
        assert "already exists" in error_message.lower(), "Should show email already exists error"
        
    finally:
        driver.quit()


def test_registration_with_password_mismatch():
    """Test registration when password and confirm password don't match"""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    # Load test data from config
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    test_data = config['test_data']['registration']['password_mismatch']
    
    try:
        registration_page.open()
        registration_page.enter_username(test_data['username'])
        registration_page.enter_email(test_data['email'])
        registration_page.enter_password(test_data['password'])
        registration_page.enter_confirm_password(test_data['confirm_password'])
        registration_page.click_register_button()
        
        # Assertion
        error_message = registration_page.get_error_message()
        assert "password" in error_message.lower() and "match" in error_message.lower(), "Should show password mismatch error"
        
    finally:
        driver.quit()


def test_registration_with_invalid_email_format():
    """Test registration with invalid email format"""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    # Load test data from config
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    test_data = config['test_data']['registration']['invalid_email']
    
    try:
        registration_page.open()
        registration_page.enter_username(test_data['username'])
        registration_page.enter_email(test_data['email'])
        registration_page.enter_password(test_data['password'])
        registration_page.enter_confirm_password(test_data['password'])
        registration_page.click_register_button()
        
        # Assertion
        error_message = registration_page.get_error_message()
        assert "email" in error_message.lower() and "invalid" in error_message.lower(), "Should show invalid email error"
        
    finally:
        driver.quit()


def test_registration_with_empty_fields():
    """Test registration with empty required fields"""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    try:
        registration_page.open()
        registration_page.click_register_button()
        
        # Assertion
        error_message = registration_page.get_error_message()
        assert "required" in error_message.lower() or "fill" in error_message.lower(), "Should show required fields error"
        
    finally:
        driver.quit()
