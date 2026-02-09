# ProfilePage.py
"""
Page Object Model for the Profile Page (Selenium version)
Author: [Your Name]
Description: This class encapsulates interactions with the Profile Page using Selenium.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProfilePage:
    USER_PROFILE_ICON = (By.CSS_SELECTOR, ".user-profile-name")  # From Locators.json

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    def click_profile(self):
        """
        Clicks the user profile icon.
        """
        profile_icon = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.USER_PROFILE_ICON)
        )
        profile_icon.click()
