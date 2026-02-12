# tests/ui/test_registration_with_existing_email.py

from pages.registration_page import RegistrationPage
from pages.confirmation_page import ConfirmationPage
from core.driver_factory import get_driver


def test_registration_with_existing_email():
 """
 Test registration flow with an existing email to verify duplicate email error handling.
 
 Steps:
 1. Navigate to registration page
 2. Enter email and submit registration
 3. Verify confirmation page is displayed
 4. Navigate back to registration page
 5. Attempt to register with the same email
 6. Verify error message for duplicate email is displayed
 """
 driver = get_driver()
 
 try:
 # Initialize page objects
 registration_page = RegistrationPage(driver)
 confirmation_page = ConfirmationPage(driver)
 
 # Step 1: Navigate to registration page
 registration_page.open()
 
 # Step 2: Enter email and submit registration
 test_email = "test.user@example.com"
 registration_page.enter_email(test_email)
 registration_page.submit_registration()
 
 # Step 3: Verify confirmation page is displayed
 assert confirmation_page.is_confirmation_displayed(), "Confirmation page should be displayed after registration"
 
 # Step 4: Navigate back to registration page
 registration_page.open()
 
 # Step 5: Attempt to register with the same email
 registration_page.enter_email(test_email)
 registration_page.submit_registration()
 
 # Step 6: Verify error message for duplicate email
 assert registration_page.is_error_displayed(), "Error message should be displayed for duplicate email"
 error_message = registration_page.get_error_message()
 assert "already exists" in error_message.lower() or "already registered" in error_message.lower(), \
 f"Expected duplicate email error message, but got: {error_message}"
 
 finally:
 driver.quit()
