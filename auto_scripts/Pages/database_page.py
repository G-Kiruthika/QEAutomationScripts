# auto_scripts/Pages/database_page.py

from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class DatabasePage(BasePage):
    # Locators
    DB_NAME_INPUT = (By.ID, "dbNameInput")
    DB_SUBMIT_BUTTON = (By.XPATH, "//button[@id='dbSubmit']")
    DB_STATUS_LABEL = (By.CSS_SELECTOR, ".db-status-label")

    # Actions
    def enter_database_name(self, name):
        self.enter_text(self.DB_NAME_INPUT, name)

    def click_submit(self):
        self.click(self.DB_SUBMIT_BUTTON)

    # Validations
    def is_status_label_visible(self):
        return self.is_visible(self.DB_STATUS_LABEL)
