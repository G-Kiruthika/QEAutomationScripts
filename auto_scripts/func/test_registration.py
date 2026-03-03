import pytest
import yaml
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.registration_page import RegistrationPage
from core.driver_factory import get_driver
from core.selenium_wrapper import SeleniumWrapper
from utils.send_email_report import send_report

class TestRegistration:
    """Test suite for user registration functionality"""
    
    @pytest.fixture(scope="function")
    def setup(self):
        """Setup test environment"""
        with open('config/config.yaml') as f:
            self.config = yaml.safe_load(f)
        self.driver = get_driver(self.config['browser'])
        self.registration_page = RegistrationPage(self.driver)
        yield
        self.driver.quit()
    
    def test_registration_valid_user(self, setup):
        """Test successful user registration with valid data"""
        try:
            self.registration_page.navigate_to_registration()
            self.registration_page.fill_registration_form(
                username="testuser123",
                email="testuser@example.com",
                password="SecurePass123!",
                confirm_password="SecurePass123!"
            )
            self.registration_page.submit_registration()
            
            success_message = self.registration_page.get_success_message()
            assert "Registration successful" in success_message, "Registration should be successful"
            
        except Exception as e:
            send_report(f"Registration test failed: {str(e)}")
            raise
    
    def test_registration_invalid_email(self, setup):
        """Test registration with invalid email format"""
        try:
            self.registration_page.navigate_to_registration()
            self.registration_page.fill_registration_form(
                username="testuser123",
                email="invalid-email",
                password="SecurePass123!",
                confirm_password="SecurePass123!"
            )
            self.registration_page.submit_registration()
            
            error_message = self.registration_page.get_error_message()
            assert "Invalid email format" in error_message, "Should show invalid email error"
            
        except Exception as e:
            send_report(f"Invalid email test failed: {str(e)}")
            raise
    
    def test_registration_password_mismatch(self, setup):
        """Test registration with mismatched passwords"""
        try:
            self.registration_page.navigate_to_registration()
            self.registration_page.fill_registration_form(
                username="testuser123",
                email="testuser@example.com",
                password="SecurePass123!",
                confirm_password="DifferentPass456!"
            )
            self.registration_page.submit_registration()
            
            error_message = self.registration_page.get_error_message()
            assert "Passwords do not match" in error_message, "Should show password mismatch error"
            
        except Exception as e:
            send_report(f"Password mismatch test failed: {str(e)}")
            raise
    
    def test_registration_duplicate_username(self, setup):
        """Test registration with existing username"""
        try:
            self.registration_page.navigate_to_registration()
            self.registration_page.fill_registration_form(
                username="existinguser",
                email="newemail@example.com",
                password="SecurePass123!",
                confirm_password="SecurePass123!"
            )
            self.registration_page.submit_registration()
            
            error_message = self.registration_page.get_error_message()
            assert "Username already exists" in error_message, "Should show duplicate username error"
            
        except Exception as e:
            send_report(f"Duplicate username test failed: {str(e)}")
            raise
    
    def test_registration_empty_fields(self, setup):
        """Test registration with empty required fields"""
        try:
            self.registration_page.navigate_to_registration()
            self.registration_page.submit_registration()
            
            error_message = self.registration_page.get_error_message()
            assert "Please fill all required fields" in error_message, "Should show required fields error"
            
        except Exception as e:
            send_report(f"Empty fields test failed: {str(e)}")
            raise
    
    def test_registration_weak_password(self, setup):
        """Test registration with weak password"""
        try:
            self.registration_page.navigate_to_registration()
            self.registration_page.fill_registration_form(
                username="testuser123",
                email="testuser@example.com",
                password="123",
                confirm_password="123"
            )
            self.registration_page.submit_registration()
            
            error_message = self.registration_page.get_error_message()
            assert "Password too weak" in error_message, "Should show weak password error"
            
        except Exception as e:
            send_report(f"Weak password test failed: {str(e)}")
            raise