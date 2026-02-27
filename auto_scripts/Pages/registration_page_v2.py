from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class RegistrationPage(BasePage):
    # Locators
    registration_url = "<placeholder>"
    first_name_input = (By.ID, "<placeholder>")
    last_name_input = (By.ID, "<placeholder>")
    email_input = (By.ID, "<placeholder>")
    password_input = (By.ID, "<placeholder>")
    confirm_password_input = (By.ID, "<placeholder>")
    register_button = (By.ID, "<placeholder>")
    success_message = (By.CSS_SELECTOR, "<placeholder>")
    error_message = (By.CSS_SELECTOR, "<placeholder>")
    
    def navigate_to_registration(self):
        """Navigate to the registration page."""
        self.driver.get(self.registration_url)
    
    def enter_first_name(self, first_name):
        """Enter the user's first name."""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.first_name_input)
        )
        element.clear()
        element.send_keys(first_name)
    
    def enter_last_name(self, last_name):
        """Enter the user's last name."""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.last_name_input)
        )
        element.clear()
        element.send_keys(last_name)
    
    def enter_email(self, email):
        """Enter the user's email address."""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.email_input)
        )
        element.clear()
        element.send_keys(email)
    
    def enter_password(self, password):
        """Enter the user's password."""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.password_input)
        )
        element.clear()
        element.send_keys(password)
    
    def enter_confirm_password(self, confirm_password):
        """Enter the user's confirm password."""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.confirm_password_input)
        )
        element.clear()
        element.send_keys(confirm_password)
    
    def click_register_button(self):
        """Click the Register button to submit the registration form."""
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.register_button)
        )
        element.click()
    
    def get_success_message(self):
        """Get the registration success message."""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.success_message)
        )
        return element.text
    
    def get_error_message(self):
        """Get the error message if registration fails (e.g., duplicate email)."""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.error_message)
        )
        return element.text