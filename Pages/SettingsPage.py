# Executive Summary
# SettingsPage.py offers methods for navigating and interacting with user settings post-login.
# Supports future expansion for advanced settings management.

# Detailed Analysis:
# - Used for downstream tests after login.
# - Handles settings access, validation, and update.

# Implementation Guide:
# - Use navigate_to_settings() to open settings.
# - Use update_setting() for specific changes.

# Quality Assurance Report:
# - Locator mapping verified against Locators.json.
# - Exception handling for absent elements.

# Troubleshooting Guide:
# - If settings not accessible, validate login and locator values.

# Future Considerations:
# - Add notification, privacy, and security settings automation.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SettingsPage:
    def __init__(self, driver, locators):
        self.driver = driver
        self.locators = locators['SettingsPage']
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_settings(self):
        settings_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.locators['settings_button']))
        )
        settings_btn.click()

    def update_setting(self, setting_name, value):
        setting_field = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.locators[setting_name]))
        )
        setting_field.clear()
        setting_field.send_keys(value)
        save_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.locators['save_button']))
        )
        save_btn.click()
