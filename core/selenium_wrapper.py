from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class SeleniumWrapper:
    """Wrapper class for common Selenium operations"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def wait_for_element(self, locator, timeout=10):
        """Wait for element to be present and return it"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not found within {timeout} seconds")
    
    def wait_for_element_clickable(self, locator, timeout=10):
        """Wait for element to be clickable and return it"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not clickable within {timeout} seconds")
    
    def click_element(self, locator, timeout=10):
        """Click on element after waiting for it to be clickable"""
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
        return element
    
    def enter_text(self, locator, text, timeout=10):
        """Enter text into element after waiting for it"""
        element = self.wait_for_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        return element
    
    def get_text(self, locator, timeout=10):
        """Get text from element"""
        element = self.wait_for_element(locator, timeout)
        return element.text
    
    def is_element_present(self, locator):
        """Check if element is present"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def hover_over_element(self, locator, timeout=10):
        """Hover over element"""
        element = self.wait_for_element(locator, timeout)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        return element
    
    def scroll_to_element(self, locator, timeout=10):
        """Scroll to element"""
        element = self.wait_for_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return element