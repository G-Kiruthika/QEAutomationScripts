from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class UserProfilePage(BasePage):
    PROFILE_PICTURE = (By.XPATH, "//img[@alt='Profile Picture']")
    EDIT_BUTTON = (By.ID, 'edit-profile')
    SAVE_BUTTON = (By.ID, 'save-profile')

    def click_edit(self):
        self.driver.find_element(*self.EDIT_BUTTON).click()

    def update_profile(self, new_profile_data):
        # Example: Assume there are fields to update, this is a stub
        for field, value in new_profile_data.items():
            elem = self.driver.find_element(By.NAME, field)
            elem.clear()
            elem.send_keys(value)

    def click_save(self):
        self.driver.find_element(*self.SAVE_BUTTON).click()

    def is_profile_updated(self):
        # Example: Check for confirmation message or updated data
        return len(self.driver.find_elements(By.CSS_SELECTOR, ".profile-updated")) > 0

    def is_edit_mode_active(self):
        # Example: Check for edit mode indicator
        return len(self.driver.find_elements(By.CSS_SELECTOR, ".edit-mode")) > 0
