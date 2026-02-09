# SettingsPage.py
"""
Page Object Model for the Settings Page (Selenium version)
Author: [Your Name]
Description: This class encapsulates interactions with the Settings Page using Selenium.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SettingsPage:
    SETTINGS_MENU = (By.ID, "settings-menu")  # Placeholder locator; update as per Locators.json if available

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    def open_settings(self):
        """
        Clicks the settings menu to open settings page.
        """
        settings_menu = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.SETTINGS_MENU)
        )
        settings_menu.click()
