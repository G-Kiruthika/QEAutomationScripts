from pages.registration_page import RegistrationPage
from pages.confirmation_page import ConfirmationPage
from core.driver_factory import get_driver


def test_registration_with_existing_email():
 """
 Test Case C39: Registration with existing email
 Validates that attempting to register with an existing email shows an error.
 """
 driver = get_driver()
 
 try:
 # Initialize page objects
 registration_page = RegistrationPage(driver)
 confirmation_page = ConfirmationPage(driver)
 
 # Step 1: Enter email for first registration
 registration_page.enter_email("user@example.com")
 
 # Step 2: Submit registration
 registration_page.submit_registration()
 
 # Step 3: Assert confirmation is displayed
 assert confirmation_page.is_confirmation_text_correct(), "Confirmation should be displayed after first registration"
 
 # Step 4: Enter the same email again
 registration_page.enter_email("user@example.com")
 
 # Step 5: Submit registration again
 registration_page.submit_registration()
 
 # Step 6: Assert error is displayed for duplicate registration
 assert registration_page.is_error_displayed(), "Error message should be displayed when registering with existing email"
 
 finally:
 driver.quit()