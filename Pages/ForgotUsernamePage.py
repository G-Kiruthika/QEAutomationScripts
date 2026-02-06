# ForgotUsernamePage.py

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ForgotUsernamePage:
    """
    Page Object for the 'Forgot Username' workflow in the login process.
    Assumes the existence of a 'Forgot Username' link on the LoginPage.
    """

    URL = 'https://example-ecommerce.com/login'

    # Locators (update these with actual values from your application)
    FORGOT_USERNAME_LINK = (By.CSS_SELECTOR, "a.forgot-username-link")
    INSTRUCTIONS_CONTAINER = (By.CSS_SELECTOR, "div.forgot-username-instructions")
    EMAIL_INPUT = (By.ID, "forgot-username-email")
    SUBMIT_BUTTON = (By.ID, "forgot-username-submit")
    USERNAME_RESULT = (By.CSS_SELECTOR, "span.recovered-username")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_login(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.FORGOT_USERNAME_LINK))

    def click_forgot_username_link(self):
        link = self.wait.until(EC.element_to_be_clickable(self.FORGOT_USERNAME_LINK))
        link.click()
        self.wait.until(EC.visibility_of_element_located(self.INSTRUCTIONS_CONTAINER))

    def follow_instructions_and_recover_username(self, email):
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()

    def get_recovered_username(self):
        try:
            username_elem = self.wait.until(EC.visibility_of_element_located(self.USERNAME_RESULT))
            return username_elem.text
        except Exception:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            raise Exception(f"Username recovery failed: {error_elem.text}")
