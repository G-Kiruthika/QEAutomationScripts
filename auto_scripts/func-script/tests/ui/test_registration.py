import pytest
from pages.registration_page import RegistrationPage
from core.driver_factory import get_driver
from utils.send_email_report import send_report


class TestRegistration:
    """Test suite for user registration functionality"""
    
    def setup_method(self):
        """Setup method to initialize driver and page object"""
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
        try:
            # Test data
            first_name = "John"
            last_name = "Doe"
            email = "john.doe@example.com"
            password = "Password123"
            confirm_password = "Password123"
            
            # Test flow
            self.registration_page.navigate_to_registration()
            self.registration_page.enter_first_name(first_name)
            self.registration_page.enter_last_name(last_name)
            self.registration_page.enter_email(email)
            self.registration_page.enter_password(password)
            self.registration_page.enter_confirm_password(confirm_password)
            self.registration_page.click_register_button()
            
            # Verification
            success_message = self.registration_page.get_success_message()
            assert self.registration_page.is_success_message_visible(), "Success message should be visible"
            assert success_message is not None, "Success message should not be None"
            
        except Exception as e:
            send_report(f"test_user_registration failed: {str(e)}")
            raise
    
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.registration
    @pytest.mark.validation
    def test_registration_with_duplicate_email(self):
        """Verify that registration fails if the email address is already registered."""
        try:
            # Test data
            first_name = "Jane"
            last_name = "Smith"
            email = "john.doe@example.com"  # Duplicate email
            password = "Password123"
            confirm_password = "Password123"
            
            # Test flow
            self.registration_page.navigate_to_registration()
            self.registration_page.enter_first_name(first_name)
            self.registration_page.enter_last_name(last_name)
            self.registration_page.enter_email(email)
            self.registration_page.enter_password(password)
            self.registration_page.enter_confirm_password(confirm_password)
            self.registration_page.click_register_button()
            
            # Verification
            error_message = self.registration_page.get_error_message()
            assert self.registration_page.is_error_message_visible(), "Error message should be visible"
            assert error_message is not None, "Error message should not be None"
            assert "already registered" in error_message.lower() or "duplicate" in error_message.lower(), "Error message should indicate duplicate email"
            
        except Exception as e:
            send_report(f"test_registration_with_duplicate_email failed: {str(e)}")
            raise