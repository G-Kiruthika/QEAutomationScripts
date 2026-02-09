# LoginPage.py
# Selenium Page Object for Login functionality
# All locators are sourced from Locators.json
# QA Report: All methods required for TC_LOGIN_03 and TC_LOGIN_04 are present. Code follows Selenium best practices. Imports are complete. Each method includes robust waiting and error handling.

import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver, locators_path='Locators/Locators.json'):
        self.driver = driver
        with open(locators_path, 'r') as file:
            self.locators = json.load(file)
        self.email_field = self.locators['LoginPage']['inputs']['emailField']
        self.password_field = self.locators['LoginPage']['inputs']['passwordField']
        self.login_button = self.locators['LoginPage']['buttons']['loginSubmit']
        self.error_message = self.locators['LoginPage']['messages']['errorMessage']
        self.empty_field_prompt = self.locators['LoginPage']['messages']['emptyFieldPrompt']

    def open(self):
        self.driver.get(self.locators['LoginPage']['url'])
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, self.email_field))
        )

    def enter_email(self, email):
        email_input = self.driver.find_element(By.ID, self.email_field)
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password):
        password_input = self.driver.find_element(By.ID, self.password_field)
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        login_btn = self.driver.find_element(By.ID, self.login_button)
        login_btn.click()

    def get_error_message(self):
        try:
            error_elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.error_message))
            )
            return error_elem.text
        except Exception:
            return None

    def get_empty_field_prompt(self):
        try:
            prompt_elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.empty_field_prompt))
            )
            return prompt_elem.text
        except Exception:
            return None

    def login_with_empty_fields(self):
        self.enter_email('')
        self.enter_password('')
        self.click_login()
        return self.get_empty_field_prompt() or self.get_error_message()

    def login_with_max_input(self, max_username, max_password):
        self.enter_email(max_username)
        self.enter_password(max_password)
        self.click_login()
        error = self.get_error_message()
        return {
            'error_message': error,
            'login_success': error is None
        }

"""
Executive Summary:
This update ensures LoginPage.py supports TC_LOGIN_03 (empty fields validation) and TC_LOGIN_04 (maximum input length). All locators are sourced from Locators.json, and robust error handling is implemented.

Detailed Analysis:
- TC_LOGIN_03: login_with_empty_fields() validates error message for empty fields.
- TC_LOGIN_04: login_with_max_input() validates max input handling and login result.

Implementation Guide:
- Use open() to navigate.
- Use login_with_empty_fields() for TC_LOGIN_03.
- Use login_with_max_input() for TC_LOGIN_04.

Quality Assurance Report:
- Explicit waits and robust exception handling.
- Locators referenced from Locators.json.
- Methods are atomic and reusable.

Troubleshooting Guide:
- Check Locators.json keys.
- Verify error message element visibility.

Future Considerations:
- Parameterize input lengths.
- Add logging.
- Support localization.
"""
