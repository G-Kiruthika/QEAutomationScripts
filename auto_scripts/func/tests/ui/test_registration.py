"""Registration Test Suite

This module contains test cases for user registration functionality.
"""

import pytest
from core.driver_factory import get_driver
from pages.registration_page import RegistrationPage


def test_register_new_user():
    """Test successful registration of a new user.
    
    Steps:
        1. Initialize driver and registration page
        2. Enter first name: John
        3. Enter last name: Doe
        4. Enter email: john.doe@example.com
        5. Enter password: Password123
        6. Click register button
        7. Verify success message is displayed
    
    Expected Result:
        Success message is displayed.
    """
    driver = get_driver()
    try:
        registration_page = RegistrationPage(driver)
        
        # Execute test flow
        registration_page.enter_first_name("John")
        registration_page.enter_last_name("Doe")
        registration_page.enter_email("john.doe@example.com")
        registration_page.enter_password("Password123")
        registration_page.click_register_button()
        
        # Assertion
        success_message = registration_page.get_success_message()
        assert success_message is not None, "Success message is displayed."
        
    finally:
        driver.quit()


def test_register_duplicate_email():
    """Test registration with duplicate email address.
    
    Steps:
        1. Initialize driver and registration page
        2. Enter first name: Jane
        3. Enter last name: Doe
        4. Enter email: john.doe@example.com (duplicate)
        5. Enter password: Password123
        6. Click register button
        7. Verify error message for duplicate email is displayed
    
    Expected Result:
        Error message for duplicate email is displayed.
    """
    driver = get_driver()
    try:
        registration_page = RegistrationPage(driver)
        
        # Execute test flow
        registration_page.enter_first_name("Jane")
        registration_page.enter_last_name("Doe")
        registration_page.enter_email("john.doe@example.com")
        registration_page.enter_password("Password123")
        registration_page.click_register_button()
        
        # Assertion
        error_message = registration_page.get_error_message()
        assert error_message is not None, "Error message for duplicate email is displayed."
        
    finally:
        driver.quit()
