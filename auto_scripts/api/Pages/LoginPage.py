from selenium.webdriver.common.by import By
from auto_scripts.Pages.BasePage import BasePage


class LoginPage(BasePage):
    """Page Object for Login functionality"""
    
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login_button")
    ADMIN_DASHBOARD = (By.XPATH, "//h1[text()='Admin Dashboard']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[@class='success' and contains(text(), 'Login successful')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def login_as_admin(self, username, password):
        """
        Login with admin credentials
        
        Args:
            username (str): Admin username
            password (str): Admin password
        """
        self.find_element(self.USERNAME_INPUT).send_keys(username)
        self.find_element(self.PASSWORD_INPUT).send_keys(password)
        self.find_element(self.LOGIN_BUTTON).click()
    
    def assert_admin_login_successful(self):
        """
        Verify admin login was successful
        
        Returns:
            bool: True if login successful, False otherwise
        """
        return self.is_visible(self.ADMIN_DASHBOARD) or self.is_visible(self.SUCCESS_MESSAGE)
