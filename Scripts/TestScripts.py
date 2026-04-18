# Existing imports and test methods
from LoginPage import LoginPage
import pytest

# ... existing test methods ...

# TC_LOGIN_007: Test navigation to login page, click 'Forgot Password', verify redirect and presence of email input and instructions.
def test_TC_LOGIN_007_forgot_password_navigation_and_validation(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    assert login_page.is_login_page_displayed(), "Login page is not displayed."
    login_page.click_forgot_password()
    assert login_page.verify_forgot_password_elements(), "Forgot Password page does not display required elements."

# TC_LOGIN_008: Test maximum length email input, valid password entry, click login, assert login or error.
def test_TC_LOGIN_008_max_length_email_and_valid_password(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    max_length_email = login_page.enter_max_length_email()
    assert login_page.verify_email_field_accepts_max_length(), "Email field did not accept maximum length email."
    valid_password = "ValidPass123!"
    login_page.enter_password(valid_password)
    login_page.click_login()
    if login_page.is_logged_in():
        assert True, "User is logged in with maximum length email."
    else:
        error_msg = login_page.get_error_message()
        assert error_msg is not None and error_msg != "", "No error message shown for max length email login failure."

# TC_LOGIN_009: Accessibility checks (screen reader, keyboard navigation, color contrast)
def test_TC_LOGIN_009_accessibility(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    assert login_page.check_screen_reader_compatibility(), "Screen reader compatibility check failed."
    assert login_page.check_keyboard_navigation(), "Keyboard navigation check failed."
    assert login_page.check_color_contrast(), "Color contrast check failed."

# TC_LOGIN_010: Password masking check
def test_TC_LOGIN_010_password_masking(driver):
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    password = "TestPassword123!"
    login_page.enter_password(password)
    assert login_page.is_password_masked(), "Password input is not masked as expected."
