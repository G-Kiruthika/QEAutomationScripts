# LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.ID, "usernameInput")
        self.password_field = (By.ID, "passwordInput")
        self.login_button = (By.ID, "loginButton")
        self.error_message = (By.ID, "errorMessage")
        self.remember_me_checkbox = (By.ID, "rememberMeCheckbox")
        self.forgot_password_link = (By.ID, "forgotPasswordLink")
        self.forgot_username_link = (By.ID, "forgotUsernameLink")  # Assumed locator from Locators.json
        self.recovery_instruction = (By.ID, "recoveryInstruction")  # Assumed locator
        self.username_display = (By.ID, "usernameDisplay")         # Assumed locator for retrieved username

    def enter_username(self, username):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_field)
        ).clear()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_field)
        ).send_keys(username)

    def enter_password(self, password):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_field)
        ).clear()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_field)
        ).send_keys(password)

    def click_login(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        ).click()

    def get_error_message(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.error_message)
        ).text

    def is_remember_me_checkbox_present(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.remember_me_checkbox)
        ) is not None

    # --- New methods for 'Forgot Username' workflow ---
    def click_forgot_username(self):
        """
        Clicks the 'Forgot Username' link on the login page.
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.forgot_username_link)
        ).click()

    def follow_recovery_instructions(self):
        """
        Follows the instructions presented after clicking 'Forgot Username'.
        """
        instruction_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.recovery_instruction)
        )
        # Example: click a button or fill in a form as per instruction
        # This is a placeholder for actual steps, which should be implemented as per real instructions
        # For demonstration, let's assume there's a button to proceed
        proceed_button = (By.ID, "proceedRecoveryButton")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(proceed_button)
        ).click()

    def retrieve_username(self):
        """
        Retrieves the username from the recovery result display.
        """
        username = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_display)
        ).text
        return username
