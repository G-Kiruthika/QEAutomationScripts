import pytest
from pages.registration_page import RegistrationPage
from core.driver_factory import get_driver
from utils.send_email_report import send_report

class TestRegistration:
    """Test class for user registration functionality."""
    
    def setup_method(self):
        """Setup method to initialize driver and page object."""
        self.driver = get_driver()
        self.registration_page = RegistrationPage(self.driver)
    
    def teardown_method(self):
        """Teardown method to close driver."""
        if self.driver:
            self.driver.quit()
    
    def test_user_registration(self):
        """Verify that a new user can successfully register with valid details."""
        try:
            # Test data
            test_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'password': 'Password123',
                'confirm_password': 'Password123'
            }
            
            # Test flow
            self.registration_page.navigate_to_registration()
            self.registration_page.enter_first_name(test_data['first_name'])
            self.registration_page.enter_last_name(test_data['last_name'])
            self.registration_page.enter_email(test_data['email'])
            self.registration_page.enter_password(test_data['password'])
            self.registration_page.enter_confirm_password(test_data['confirm_password'])
            self.registration_page.click_register_button()
            
            # Verification
            assert self.registration_page.is_success_message_visible(), "Success message should be visible"
            success_message = self.registration_page.get_success_message()
            assert "successfully" in success_message.lower() or "registered" in success_message.lower(), f"Expected success message, got: {success_message}"
            
        except Exception as e:
            send_report(f"test_user_registration failed: {str(e)}")
            raise
    
    def test_registration_with_duplicate_email(self):
        """Verify that registration fails if the email address is already registered."""
        try:
            # Test data
            test_data = {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'john.doe@example.com',
                'password': 'Password123',
                'confirm_password': 'Password123'
            }
            
            # Test flow
            self.registration_page.navigate_to_registration()
            self.registration_page.enter_first_name(test_data['first_name'])
            self.registration_page.enter_last_name(test_data['last_name'])
            self.registration_page.enter_email(test_data['email'])
            self.registration_page.enter_password(test_data['password'])
            self.registration_page.enter_confirm_password(test_data['confirm_password'])
            self.registration_page.click_register_button()
            
            # Verification
            assert self.registration_page.is_error_message_visible(), "Error message should be visible"
            error_message = self.registration_page.get_error_message()
            assert "already" in error_message.lower() or "exists" in error_message.lower(), f"Expected duplicate email error, got: {error_message}"
            
        except Exception as e:
            send_report(f"test_registration_with_duplicate_email failed: {str(e)}")
            raise