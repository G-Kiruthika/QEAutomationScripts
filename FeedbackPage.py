from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class FeedbackPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open_why_dropdown(self):
        dropdown = self.driver.find_element(By.ID, 'why-dropdown')
        dropdown.click()

    def select_why_option(self, option_text):
        option = self.driver.find_element(By.XPATH, f"//li[contains(text(), '{option_text}')]")
        option.click()

    def get_selected_option(self):
        selected = self.driver.find_element(By.ID, 'why-dropdown-selected')
        return selected.text
