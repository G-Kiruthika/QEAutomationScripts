import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver, locators):
        self.driver = driver
        self.locators = locators

    def enter_username(self, username):
        username_field = self.driver.find_element(By.XPATH, self.locators['username'])
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = self.driver.find_element(By.XPATH, self.locators['password'])
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        login_button = self.driver.find_element(By.XPATH, self.locators['login_button'])
        login_button.click()

    def get_error_message(self):
        try:
            error = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, self.locators['error_message']))
            )
            return error.text
        except:
            return None

    def is_dashboard_displayed(self):
        try:
            dashboard = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, self.locators['dashboard']))
            )
            return True
        except:
            return False

    # New method: Check for CAPTCHA presence
    def is_captcha_present(self):
        try:
            captcha = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, self.locators.get('captcha', '')))
            )
            return True
        except:
            return False

    # New method: Check for account lockout message
    def is_account_locked(self):
        try:
            lockout = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, self.locators.get('account_lockout', '')))
            )
            return True
        except:
            return False

    # New method: Validate minimum-length login
    def is_username_min_length_valid(self, min_length):
        username_field = self.driver.find_element(By.XPATH, self.locators['username'])
        return len(username_field.get_attribute('value')) >= min_length

    # New method: Validate minimum-length password
    def is_password_min_length_valid(self, min_length):
        password_field = self.driver.find_element(By.XPATH, self.locators['password'])
        return len(password_field.get_attribute('value')) >= min_length

    # New method: Attempt login and return result dict
    def attempt_login_and_analyze(self, username, password, min_username_length=0, min_password_length=0):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        time.sleep(1)
        result = {
            'dashboard': self.is_dashboard_displayed(),
            'error_message': self.get_error_message(),
            'captcha': self.is_captcha_present(),
            'account_locked': self.is_account_locked(),
            'username_min_length_valid': self.is_username_min_length_valid(min_username_length),
            'password_min_length_valid': self.is_password_min_length_valid(min_password_length)
        }
        return result
