# LoginPage.py
'''
PageClass for Login Page
Handles login screen navigation and interaction, including 'Forgot Username' link.
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.username_field = driver.find_element(By.ID, 'username')  # Example locator
        self.password_field = driver.find_element(By.ID, 'password')  # Example locator
        self.login_button = driver.find_element(By.ID, 'loginBtn')    # Example locator
        self.forgot_username_link = driver.find_element(By.LINK_TEXT, 'Forgot Username')  # Strict locator

    def navigate_to_login_screen(self, url):
        '''Navigates to the login screen.'''
        self.driver.get(url)

    def click_forgot_username(self):
        '''Clicks the 'Forgot Username' link.'''
        self.forgot_username_link.click()

    # Existing login methods remain unchanged
