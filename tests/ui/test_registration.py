import pytest
from selenium import webdriver
from pages.registration_page import RegistrationPage
from core.driver_factory import get_driver
from utils.send_email_report import send_email_report
import yaml
import os

class TestRegistration:
    """Test class for user registration functionality"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup method to initialize driver and page objects"""
        self.driver = get_driver()
        self.registration_page = RegistrationPage(self.driver)
        
        # Load configuration
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        yield
        
        # Teardown
        if self.driver:
            self.driver.quit()
    
    def test_user_registration(self):
        """
        Test Case: Verify that a new user can successfully register with valid details
        Expected Result: User is registered successfully and sees a confirmation message
        """
        # Test data
        test_data = {
            'first_name': 'John',
            'last_name': 'Doe', 
            'email': 'john.doe@example.com',
            'password': 'Password123',
            'confirm_password': 'Password123'
        }
        
        try:
            # Navigate to registration page
            self.registration_page.navigate_to_registration()
            
            # Fill registration form
            self.registration_page.enter_first_name(test_data['first_name'])
            self.registration_page.enter_last_name(test_data['last_name'])
            self.registration_page.enter_email(test_data['email'])
            self.registration_page.enter_password(test_data['password'])
            self.registration_page.enter_confirm_password(test_data['confirm_password'])
            
            # Submit registration
            self.registration_page.click_register_button()
            
            # Verify success message
            assert self.registration_page.is_success_message(), "Success message should be visible"
            success_message = self.registration_page.get_success_message()
            assert "successfully" in success_message.lower(), f"Expected success message, got: {success_message}"
            
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")
    
    def test_registration_with_duplicate_email(self):
        """
        Test Case: Verify that registration fails if the email address is already registered
        Expected Result: Error message is displayed indicating the email is already registered
        """
        # Test data with duplicate email
        test_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'john.doe@example.com',  # Duplicate email
            'password': 'Password123',
            'confirm_password': 'Password123'
        }
        
        try:
            # Navigate to registration page
            self.registration_page.navigate_to_registration()
            
            # Fill registration form
            self.registration_page.enter_first_name(test_data['first_name'])
            self.registration_page.enter_last_name(test_data['last_name'])
            self.registration_page.enter_email(test_data['email'])
            self.registration_page.enter_password(test_data['password'])
            self.registration_page.enter_confirm_password(test_data['confirm_password'])
            
            # Submit registration
            self.registration_page.click_register_button()
            
            # Verify error message
            assert self.registration_page.is_error_message(), "Error message should be visible"
            error_message = self.registration_page.get_error_message()
            assert "already registered" in error_message.lower() or "email exists" in error_message.lower(), \
                f"Expected duplicate email error message, got: {error_message}"
                
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")