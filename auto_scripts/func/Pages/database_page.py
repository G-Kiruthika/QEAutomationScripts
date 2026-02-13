from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DatabasePage(BasePage):
    USER_RECORD = (By.DB, 'user_record_placeholder')
    PASSWORD_HASH = (By.DB, 'password_hash_placeholder')

    def __init__(self, driver):
        super().__init__(driver)

    def retrieve_user_record(self, email):
        # Wrapper method from BasePage assumed: get_db_record(locator, key)
        return self.get_db_record(self.USER_RECORD, email)

    def validate_password_hash(self):
        # Wrapper method from BasePage assumed: is_db_record_visible(locator)
        return self.is_db_record_visible(self.PASSWORD_HASH)
