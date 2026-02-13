from pages.registration_page import RegistrationPage
from pages.database_page import DatabasePage
from core.driver_factory import get_driver

def test_register_new_user_and_verify_password_storage():
    """Test case C42: Register new user and verify password storage in database"""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    database_page = DatabasePage(driver)
    
    # Test data
    user_data = {
        "email": "user@example.com",
        "password": "SecurePass123",
        "name": "John Doe"
    }
    
    # Execute test flow
    registration_page.register_user(
        email=user_data["email"],
        password=user_data["password"],
        name=user_data["name"]
    )
    
    # Assertion: validate registration success
    assert registration_page.validate_registration_success(), "Registration should be successful"
    
    # Retrieve user record from database
    user_record = database_page.retrieve_user_record(user_data["email"])
    
    # Assertion: validate password hash
    assert database_page.validate_password_hash(), "Password hash should be stored correctly"
    
    driver.quit()

def test_register_with_valid_and_invalid_details():
    """Test case C43: Register with valid and invalid details"""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    # Test data - valid user
    user_data_valid = {
        "email": "user@example.com",
        "password": "SecurePass123",
        "name": "John Doe"
    }
    
    # Test data - invalid user
    user_data_invalid = {
        "email": "user@example.com"
    }
    
    # Execute test flow - valid registration
    registration_page.register_user(
        email=user_data_valid["email"],
        password=user_data_valid["password"],
        name=user_data_valid["name"]
    )
    
    # Assertion: validate registration success
    assert registration_page.validate_registration_success(), "Valid registration should be successful"
    
    # Execute test flow - invalid registration
    registration_page.register_user(
        email=user_data_invalid["email"]
    )
    
    # Assertion: validate error message
    assert registration_page.validate_error_message(), "Invalid registration should show error message"
    
    driver.quit()
