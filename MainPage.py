from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class MainPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def is_loaded(self) -> bool:
        # Replace with the actual locator for the main screen
        return True

    def tap_profile_icon(self):
        profile_icon = self.driver.find_element(By.CSS_SELECTOR, '.user-profile-name')
        profile_icon.click()
