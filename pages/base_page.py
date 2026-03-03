from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from core.selenium_wrapper import SeleniumWrapper

class BasePage:
    """Base page class with common functionality for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.selenium_wrapper = SeleniumWrapper(driver)
    
    def wait_for_element(self, locator, timeout=10):
        """Wait for element to be present"""
        return self.selenium_wrapper.wait_for_element(locator, timeout)
    
    def click_element(self, locator):
        """Click on element"""
        return self.selenium_wrapper.click_element(locator)
    
    def enter_text(self, locator, text):
        """Enter text into element"""
        return self.selenium_wrapper.enter_text(locator, text)
    
    def get_text(self, locator):
        """Get text from element"""
        element = self.wait_for_element(locator)
        return element.text
    
    def is_element_visible(self, locator):
        """Check if element is visible"""
        try:
            element = self.wait_for_element(locator)
            return element.is_displayed()
        except:
            return False
    
    def navigate_to(self, url):
        """Navigate to specified URL"""
        self.driver.get(url)