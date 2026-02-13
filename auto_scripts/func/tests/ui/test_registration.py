"""Registration Test Suite

This module contains automated tests for user registration functionality.
Follows the Python UI Automation Framework standards.
"""

from pages.registration_page import RegistrationPage
from core.driver_factory import get_driver
import pytest
import logging


logger = logging.getLogger(__name__)


def test_register_new_user():
    """Test successful registration of a new user.
    
    Verifies that a new user can register with valid credentials
    and receives a success message.
    """
    driver = get_driver()
    try:
        registration_page = RegistrationPage(driver)
        
        # Execute registration flow
        registration_page.enter_first_name("John")
        registration_page.enter_last_name("Doe")
        registration_page.enter_email("john.doe@example.com")
        registration_page.enter_password("Password123")
        registration_page.click_register_button()
        
        # Verify success message
        success_message = registration_page.get_success_message()
        assert success_message is not None, "Success message is displayed."
        
        logger.info("Test test_register_new_user passed successfully")
    except Exception as e:
        logger.error(f"Test test_register_new_user failed: {str(e)}")
        raise
    finally:
        driver.quit()


def test_register_duplicate_email():
    """Test registration with duplicate email address.
    
    Verifies that attempting to register with an existing email
    displays an appropriate error message.
    """
    driver = get_driver()
    try:
        registration_page = RegistrationPage(driver)
        
        # Execute registration flow with duplicate email
        registration_page.enter_first_name("Jane")
        registration_page.enter_last_name("Doe")
        registration_page.enter_email("john.doe@example.com")
        registration_page.enter_password("Password123")
        registration_page.click_register_button()
        
        # Verify error message
        error_message = registration_page.get_error_message()
        assert error_message is not None, "Error message for duplicate email is displayed."
        
        logger.info("Test test_register_duplicate_email passed successfully")
    except Exception as e:
        logger.error(f"Test test_register_duplicate_email failed: {str(e)}")
        raise
    finally:
        driver.quit()
