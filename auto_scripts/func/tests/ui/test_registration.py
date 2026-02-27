import pytest
from pages.registration_page import RegistrationPage
from core.driver_factory import get_driver


class TestRegistration:
    """Test suite for user registration functionality."""
    
    def setup_method(self):
        """Setup method to initialize driver and page objects."""
        self.driver = get_driver()
        self.registration_page = RegistrationPage(self.driver)
    
    def teardown_method(self):
        """Teardown method to clean up driver."""
        if self.driver:
            self.driver.quit()
    
    def test_registration_with_valid_details(self):
        """Test C38: Registration with valid user details."""
        # Test data
        user_data = {
            "email": "user@example.com",
            "password": "SecurePass123",
            "name": "John Doe"
        }
        
        # Test flow
        assert self.registration_page.validate_registration_page_displayed(), "Registration page should be displayed"
        
        self.registration_page.enter_email(user_data["email"])
        self.registration_page.enter_password(user_data["password"])
        self.registration_page.enter_name(user_data["name"])
        self.registration_page.submit_registration()
        
        assert self.registration_page.validate_registration_success(), "Registration should be successful"
    
    def test_registration_with_duplicate_email(self):
        """Test C39: Registration with duplicate email address."""
        # Test data
        user_data = {
            "email": "user@example.com"
        }
        
        # Test flow
        self.registration_page.enter_email(user_data["email"])
        self.registration_page.submit_registration()
        
        assert self.registration_page.validate_registration_success(), "First registration should be successful"
        
        # Attempt duplicate registration
        self.registration_page.enter_email(user_data["email"])
        self.registration_page.submit_registration()
        
        assert self.registration_page.validate_error_message("Email already exists."), "Error message should display for duplicate email"