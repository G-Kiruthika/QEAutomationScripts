from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class LoginPage(BasePage):
    # Existing locators (if any) would be preserved here

    # --- Locators from metadata (append only missing, no duplicates) ---
    username_field = (By.ID, "username_field")  # Placeholder locator
    password_field = (By.ID, "password_field")  # Placeholder locator
    login_button = (By.ID, "login_button")      # Placeholder locator
    validation_error_message = (By.ID, "validation_error_message")  # Placeholder locator
    account_lockout_message = (By.ID, "account_lockout_message")    # Placeholder locator
    email_notification = (By.ID, "email_notification")              # Placeholder locator

    # --- Action methods from metadata (append only missing, no duplicates) ---
    def navigate_to_login_page(self):
        """
        Navigates to the login page using BasePage's navigation wrapper.
        """
        self.navigate("/login")  # Replace with actual URL or route

    def enter_username(self, username):
        """
        Enters the username in the username field using BasePage's wrapper.
        """
        self.enter_text(self.username_field, username)

    def enter_password(self, password):
        """
        Enters the password in the password field using BasePage's wrapper.
        """
        self.enter_text(self.password_field, password)

    def click_login_button(self):
        """
        Clicks the login button using BasePage's click wrapper.
        """
        self.click(self.login_button)

    def get_validation_error_message(self):
        """
        Retrieves the validation error message text using BasePage's get_text wrapper.
        """
        return self.get_text(self.validation_error_message)

    def get_account_lockout_message(self):
        """
        Retrieves the account lockout message text using BasePage's get_text wrapper.
        """
        return self.get_text(self.account_lockout_message)

    def verify_email_notification_sent(self):
        """
        Verifies if the email notification element is present using BasePage's is_element_present wrapper.
        """
        return self.is_element_present(self.email_notification)

# End of login_page.py
