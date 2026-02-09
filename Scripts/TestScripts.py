import unittest
from selenium import webdriver
from Pages.LoginPage import LoginPage

class TestLogin(unittest.TestCase):

    # Existing test methods...
    # (Assume all previous content remains unchanged)

    def test_TC_LOGIN_006_remember_me_auto_login(self):
        """TC_LOGIN_006: Valid login with 'Remember Me' checked, browser close/reopen, auto-login check."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login_with_remember_me(email="valid_user@example.com", password="valid_password")
        login_page.assert_user_logged_in()
        driver.quit()

        # Simulate browser reopen for auto-login check
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.navigate_to_home()
        login_page.assert_remember_me_auto_login()
        driver.quit()

    def test_TC_LOGIN_04_invalid_login_error(self):
        """TC-LOGIN-04: Invalid login with wrong email/password, error message validation."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login_with_invalid_credentials(email="wrong_user@example.com", password="wrong_password")
        login_page.assert_login_failed(expected_error="Invalid email or password.")
        driver.quit()

    def test_TC_LOGIN_007_forgot_password_flow(self):
        """TC_LOGIN_007: Forgot Password flow - submit password reset for registered email, verify confirmation."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        login_page.click_forgot_password_link()
        login_page.enter_forgot_password_email("user@example.com")
        login_page.submit_password_reset()
        confirmation_message = login_page.get_password_reset_confirmation()
        self.assertIsNotNone(confirmation_message, "Password reset confirmation message should be present.")
        self.assertIn("reset link has been sent", confirmation_message.lower(), "Confirmation message should indicate reset link sent.")
        driver.quit()

    def test_TC_LOGIN_05_login_with_empty_email(self):
        """TC-LOGIN-05: Login with empty email - verify error message indicating email is required."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        login_page.enter_email("")
        login_page.enter_password("ValidPassword123!")
        login_page.submit_login()
        # Check for empty field prompt or specific error message
        empty_prompt_present = login_page.is_empty_field_prompt_present()
        error_message = login_page.get_error_message()
        self.assertTrue(empty_prompt_present or (error_message and "email" in error_message.lower()), "Should show prompt or error message for empty email field.")
        driver.quit()

    # --- Appended test for TC_LOGIN_009 ---
    def test_TC_LOGIN_009_password_length_validation(self):
        """TC_LOGIN_009: Password length validation scenarios."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()

        # Step 2: Enter password with less than minimum allowed characters
        login_page.enter_email("valid_user@example.com")
        login_page.enter_password("123")  # Assuming '123' is less than min length
        login_page.click_login()
        min_length_error = login_page.get_validation_error()
        self.assertIsNotNone(min_length_error, "Should show validation error for minimum password length.")

        # Step 3: Enter password with maximum allowed characters
        login_page.enter_email("valid_user@example.com")
        max_allowed_password = "A"  # Replace with actual max allowed value
        login_page.enter_password(max_allowed_password)
        login_page.click_login()
        accepted = login_page.is_dashboard_header_present()
        self.assertTrue(accepted, "Password at max allowed length should be accepted.")

        # Step 4: Enter password exceeding maximum allowed characters
        login_page.enter_email("valid_user@example.com")
        over_max_password = "A" * 65  # Example: 65 chars, assuming max allowed is less
        login_page.enter_password(over_max_password)
        login_page.click_login()
        max_length_error = login_page.get_validation_error()
        self.assertIsNotNone(max_length_error, "Should show validation error for exceeding max password length.")
        driver.quit()

    # --- Appended test for TC-LOGIN-07 ---
    def test_TC_LOGIN_07_login_with_empty_fields(self):
        """TC-LOGIN-07: Attempt login with both email and password fields empty."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        login_page.enter_email("")
        login_page.enter_password("")
        login_page.click_login()
        empty_prompt_present = login_page.is_empty_field_prompt_present()
        error_message = login_page.get_error_message()
        self.assertTrue(empty_prompt_present or (error_message and ("email" in error_message.lower() or "password" in error_message.lower())), "Should show prompt or error message for empty email and password fields.")
        driver.quit()

    # --- Appended test for TC_LOGIN_010 ---
    def test_TC_LOGIN_010_special_char_login(self):
        """TC_LOGIN_010: Login with special characters in email and password."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        login_page.enter_email("user+test@example.com")
        login_page.enter_password("!@#$%^&*()_+")
        login_page.click_login()
        # Check if logged in
        logged_in = login_page.is_logged_in()
        self.assertTrue(logged_in, "Login with special characters should succeed if credentials are valid.")
        driver.quit()

    # --- Appended test for TC-LOGIN-08 ---
    def test_TC_LOGIN_08_remember_me_session_persistence(self):
        """TC-LOGIN-08: Login with 'Remember Me' checked and verify session persistence after browser restart."""
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        login_page.enter_email("user@example.com")
        login_page.enter_password("ValidPassword123!")
        login_page.select_remember_me()
        login_page.click_login()
        # Check if logged in
        logged_in = login_page.is_logged_in()
        self.assertTrue(logged_in, "Login with 'Remember Me' should succeed.")
        driver.quit()

        # Simulate browser restart and check session persistence
        driver = webdriver.Chrome()
        login_page = LoginPage(driver)
        login_page.go_to_login_page()
        session_persistent = login_page.is_logged_in()
        self.assertTrue(session_persistent, "Session should persist after browser restart if 'Remember Me' was checked.")
        driver.quit()
