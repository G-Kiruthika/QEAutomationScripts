import pytest
from core.driver_factory import get_driver
from pages.registration_page import RegistrationPage
from utils.send_email_report import send_email_report


class TestRegistration:
    """Registration Test Suite - Comprehensive test suite for user registration functionality"""
    
    def setup_method(self):
        """Setup method to initialize driver and page objects"""
        self.driver = get_driver()
        self.registration_page = RegistrationPage(self.driver)
    
    def teardown_method(self):
        """Teardown method to clean up driver"""
        if self.driver:
            self.driver.quit()
    
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.registration
    def test_user_registration(self):
        """Verify that a new user can successfully register with valid details."""
        # Test data
        test_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "Password123",
            "confirm_password": "Password123"
        }
        
        try:
            # Execute test flow
            self.registration_page.navigate_to_registration()
            self.registration_page.enter_first_name(test_data["first_name"])
            self.registration_page.enter_last_name(test_data["last_name"])
            self.registration_page.enter_email(test_data["email"])
            self.registration_page.enter_password(test_data["password"])
            self.registration_page.enter_confirm_password(test_data["confirm_password"])
            self.registration_page.click_register_button()
            success_message = self.registration_page.get_success_message()
            
            # Assertions
            assert self.registration_page.is_success_message_visible(), "Success message should be visible"
            assert success_message is not None, "Success message should not be None"
            assert "successfully" in success_message.lower() or "registered" in success_message.lower(), "Success message should indicate successful registration"
            
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")
    
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.registration
    @pytest.mark.validation
    def test_registration_with_duplicate_email(self):
        """Verify that registration fails if the email address is already registered."""
        # Test data
        test_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "john.doe@example.com",
            "password": "Password123",
            "confirm_password": "Password123"
        }
        
        try:
            # Execute test flow
            self.registration_page.navigate_to_registration()
            self.registration_page.enter_first_name(test_data["first_name"])
            self.registration_page.enter_last_name(test_data["last_name"])
            self.registration_page.enter_email(test_data["email"])
            self.registration_page.enter_password(test_data["password"])
            self.registration_page.enter_confirm_password(test_data["confirm_password"])
            self.registration_page.click_register_button()
            error_message = self.registration_page.get_error_message()
            
            # Assertions
            assert self.registration_page.is_error_message_visible(), "Error message should be visible"
            assert error_message is not None, "Error message should not be None"
            assert "already" in error_message.lower() or "exists" in error_message.lower() or "duplicate" in error_message.lower(), "Error message should indicate email already exists"
            
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")