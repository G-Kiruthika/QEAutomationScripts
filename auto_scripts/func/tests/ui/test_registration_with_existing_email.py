from core.driver_factory import get_driver
from pages.registration_page import RegistrationPage
from pages.confirmation_page import ConfirmationPage

def test_registration_with_existing_email():
 driver = get_driver()
 registration_page = RegistrationPage(driver)
 confirmation_page = ConfirmationPage(driver)
 # First registration attempt
 registration_page.enter_email('user@example.com')
 registration_page.submit_registration()
 assert confirmation_page.is_confirmation_text_correct() or registration_page.is_confirmation_displayed()
 # Second registration attempt with same email
 registration_page.enter_email('user@example.com')
 registration_page.submit_registration()
 assert registration_page.is_error_displayed()
 driver.quit()
