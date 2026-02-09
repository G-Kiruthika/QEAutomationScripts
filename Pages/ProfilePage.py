# Executive Summary
# ProfilePage.py provides methods to verify login success and interact with user profile elements.
# Implements robust element access and validation post-login.

# Detailed Analysis:
# - Used as landing page for TC_LOGIN_001 (valid login).
# - Validates user presence, profile info, logout functionality.

# Implementation Guide:
# - Use is_profile_loaded() to verify successful login.
# - Use get_profile_name() to fetch username.
# - Use logout() for session termination.

# Quality Assurance Report:
# - Strict locator mapping from Locators.json.
# - Exception handling for missing elements.

# Troubleshooting Guide:
# - If profile not loaded, check login flow and locator values.

# Future Considerations:
# - Add edit profile, avatar upload, and settings navigation.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProfilePage:
    def __init__(self, driver, locators):
        self.driver = driver
        self.locators = locators['ProfilePage']
        self.wait = WebDriverWait(self.driver, 10)

    def is_profile_loaded(self):
        try:
            indicator = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.locators['profile_page_indicator']))
            )
            return True
        except Exception:
            return False

    def get_profile_name(self):
        try:
            name_elem = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, self.locators['profile_name']))
            )
            return name_elem.text
        except Exception:
            return None

    def logout(self):
        logout_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, self.locators['logout_button']))
        )
        logout_btn.click()
