from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auto_scripts.Pages.base_page import BasePage


class RegistrationPage(BasePage):
    """
    RegistrationPage class for handling user registration functionality.
    Inherits from BasePage and implements all registration-related locators and methods.
    """
    
    def __init__(self, driver):
        """
        Initialize RegistrationPage with WebDriver instance.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)
    
    # Locators - All in UPPER_CASE as per requirements
    REGISTRATION_URL = "/register"
    FIRST_NAME_INPUT = (By.ID, "firstName")
    LAST_NAME_INPUT = (By.ID, "lastName")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "confirmPassword")
    REGISTER_BUTTON = (By.XPATH, "//button[@type='submit' and contains(text(), 'Register')]")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    # Navigation Methods - snake_case as per requirements
    def navigate_to_registration_page(self):
        """
        Navigate to the registration page using the registration URL.
        """
        current_url = self.driver.current_url
        if not current_url.endswith(self.REGISTRATION_URL):
            base_url = current_url.split('/')[0] + '//' + current_url.split('/')[2]
            full_url = base_url + self.REGISTRATION_URL
            self.driver.get(full_url)
        return self
    
    # Input Methods - snake_case as per requirements
    def enter_first_name(self, first_name):
        """
        Enter first name in the first name input field.
        
        Args:
            first_name (str): First name to enter
        """
        element = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_INPUT))
        element.clear()
        element.send_keys(first_name)
        return self
    
    def enter_last_name(self, last_name):
        """
        Enter last name in the last name input field.
        
        Args:
            last_name (str): Last name to enter
        """
        element = self.wait.until(EC.element_to_be_clickable(self.LAST_NAME_INPUT))
        element.clear()
        element.send_keys(last_name)
        return self
    
    def enter_email(self, email):
        """
        Enter email in the email input field.
        
        Args:
            email (str): Email address to enter
        """
        element = self.wait.until(EC.element_to_be_clickable(self.EMAIL_INPUT))
        element.clear()
        element.send_keys(email)
        return self
    
    def enter_password(self, password):
        """
        Enter password in the password input field.
        
        Args:
            password (str): Password to enter
        """
        element = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_INPUT))
        element.clear()
        element.send_keys(password)
        return self
    
    def enter_confirm_password(self, confirm_password):
        """
        Enter confirmation password in the confirm password input field.
        
        Args:
            confirm_password (str): Confirmation password to enter
        """
        element = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_PASSWORD_INPUT))
        element.clear()
        element.send_keys(confirm_password)
        return self
    
    # Action Methods - snake_case as per requirements
    def click_register_button(self):
        """
        Click the register button to submit the registration form.
        """
        element = self.wait.until(EC.element_to_be_clickable(self.REGISTER_BUTTON))
        element.click()
        return self
    
    def fill_registration_form(self, first_name, last_name, email, password, confirm_password):
        """
        Fill the complete registration form with provided details.
        
        Args:
            first_name (str): First name
            last_name (str): Last name
            email (str): Email address
            password (str): Password
            confirm_password (str): Confirmation password
        """
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_confirm_password(confirm_password)
        return self
    
    def complete_registration(self, first_name, last_name, email, password, confirm_password):
        """
        Complete the entire registration process.
        
        Args:
            first_name (str): First name
            last_name (str): Last name
            email (str): Email address
            password (str): Password
            confirm_password (str): Confirmation password
        """
        self.fill_registration_form(first_name, last_name, email, password, confirm_password)
        self.click_register_button()
        return self
    
    # Validation Methods - snake_case as per requirements
    def is_success_message_displayed(self):
        """
        Check if success message is displayed after registration.
        
        Returns:
            bool: True if success message is displayed, False otherwise
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return element.is_displayed()
        except:
            return False
    
    def is_error_message_displayed(self):
        """
        Check if error message is displayed after registration attempt.
        
        Returns:
            bool: True if error message is displayed, False otherwise
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return element.is_displayed()
        except:
            return False
    
    def get_success_message_text(self):
        """
        Get the text of the success message.
        
        Returns:
            str: Success message text or empty string if not found
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
            return element.text
        except:
            return ""
    
    def get_error_message_text(self):
        """
        Get the text of the error message.
        
        Returns:
            str: Error message text or empty string if not found
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return element.text
        except:
            return ""
    
    def validate_registration_success(self):
        """
        Validate that registration was successful by checking for success message.
        
        Returns:
            bool: True if registration was successful, False otherwise
        """
        return self.is_success_message_displayed()
    
    def validate_registration_failure(self):
        """
        Validate that registration failed by checking for error message.
        
        Returns:
            bool: True if registration failed (error message displayed), False otherwise
        """
        return self.is_error_message_displayed()
    
    # Element Presence Validation Methods
    def is_first_name_input_present(self):
        """
        Check if first name input field is present on the page.
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.driver.find_element(*self.FIRST_NAME_INPUT)
            return True
        except:
            return False
    
    def is_last_name_input_present(self):
        """
        Check if last name input field is present on the page.
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.driver.find_element(*self.LAST_NAME_INPUT)
            return True
        except:
            return False
    
    def is_email_input_present(self):
        """
        Check if email input field is present on the page.
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.driver.find_element(*self.EMAIL_INPUT)
            return True
        except:
            return False
    
    def is_password_input_present(self):
        """
        Check if password input field is present on the page.
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.driver.find_element(*self.PASSWORD_INPUT)
            return True
        except:
            return False
    
    def is_confirm_password_input_present(self):
        """
        Check if confirm password input field is present on the page.
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.driver.find_element(*self.CONFIRM_PASSWORD_INPUT)
            return True
        except:
            return False
    
    def is_register_button_present(self):
        """
        Check if register button is present on the page.
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.driver.find_element(*self.REGISTER_BUTTON)
            return True
        except:
            return False
