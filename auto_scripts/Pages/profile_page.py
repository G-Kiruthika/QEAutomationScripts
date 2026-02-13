from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProfilePage(BasePage):
    PROFILE_PIC = (By.XPATH, "//img[@class='profile-pic']")
    EDIT_BUTTON = (By.ID, "editProfile")
    SAVE_BUTTON = (By.ID, "saveProfile")

    def __init__(self, driver):
        super().__init__(driver)

    def click_edit_profile(self):
        self.click_element(self.EDIT_BUTTON)

    def update_profile_details(self, details):
        self.enter_text(self.PROFILE_PIC, details)

    def click_save_profile(self):
        self.click_element(self.SAVE_BUTTON)

    def is_profile_updated(self):
        return self.is_element_visible(self.PROFILE_PIC)

    def is_edit_mode_enabled(self):
        return self.is_element_visible(self.EDIT_BUTTON)
