# tests/ui/test_registration.py

from pages.registration_page import RegistrationPage
from core.driver_factory import get_driver
import pytest
import logging


def test_register_new_user():
    """Test successful registration of a new user."""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    try:
        # Navigate to registration page
        registration_page.open()
        
        # Enter user details
        registration_page.enter_first_name("John")
        registration_page.enter_last_name("Doe")
        registration_page.enter_email("john.doe@example.com")
        registration_page.enter_password("Password123")
        
        # Submit registration
        registration_page.click_register_button()
        
        # Verify success message
        success_message = registration_page.get_success_message()
        assert success_message is not None, "Success message should be displayed"
        logging.info(f"Registration successful: {success_message}")
        
    except Exception as e:
        logging.error(f"Test failed: {str(e)}")
        raise
    finally:
        driver.quit()


def test_register_duplicate_email():
    """Test registration with duplicate email address."""
    driver = get_driver()
    registration_page = RegistrationPage(driver)
    
    try:
        # Navigate to registration page
        registration_page.open()
        
        # Enter user details with duplicate email
        registration_page.enter_first_name("Jane")
        registration_page.enter_last_name("Doe")
        registration_page.enter_email("john.doe@example.com")
        registration_page.enter_password("Password123")
        
        # Submit registration
        registration_page.click_register_button()
        
        # Verify error message for duplicate email
        error_message = registration_page.get_error_message()
        assert error_message is not None, "Error message for duplicate email should be displayed"
        logging.info(f"Duplicate email error displayed: {error_message}")
        
    except Exception as e:
        logging.error(f"Test failed: {str(e)}")
        raise
    finally:
        driver.quit()