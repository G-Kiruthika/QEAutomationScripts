from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class RegistrationPage(BasePage):
    EMAIL_INPUT = (By.XPATH, "//input[@id='email']")
    SUBMIT_BUTTON = (By.XPATH, "//button[@id='register']")
    ERROR_MESSAGE = (By.XPATH, "//div[@class='error']")
    CONFIRMATION_MESSAGE = (By.XPATH, "//div[@class='success']")

    # Missing locators appended below
    FIRST_NAME_INPUT = (By.XPATH, "//input[@id='first_name']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@id='last_name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@id='password']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[@class='success']")
    
    # Existing methods
    def enter_email(self, email):
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

    def submit_registration(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def is_confirmation_displayed(self):
        return self.is_element_visible(self.CONFIRMATION_MESSAGE)

    def is_error_displayed(self):
        return self.is_element_visible(self.ERROR_MESSAGE)

    # Missing methods appended below
    def enter_first_name(self, first_name):
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)

    def enter_last_name(self, last_name):
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_register_button(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def get_success_message(self):
        return self.driver.find_element(*self.SUCCESS_MESSAGE).text

    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text
