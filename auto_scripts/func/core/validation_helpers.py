from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)

class ValidationHelpers:
    """Helper class for common validation operations in test automation"""
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible"""
        wait_time = timeout if timeout else self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not visible within {wait_time} seconds")
            return None
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable"""
        wait_time = timeout if timeout else self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not clickable within {wait_time} seconds")
            return None
    
    def is_element_present(self, locator):
        """Check if element is present in DOM"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator):
        """Check if element is visible on page"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def get_element_text(self, locator):
        """Get text from element"""
        try:
            element = self.wait_for_element_visible(locator)
            if element:
                return element.text
            return None
        except Exception as e:
            logger.error(f"Error getting text from element {locator}: {str(e)}")
            return None
    
    def get_element_attribute(self, locator, attribute):
        """Get attribute value from element"""
        try:
            element = self.wait_for_element_visible(locator)
            if element:
                return element.get_attribute(attribute)
            return None
        except Exception as e:
            logger.error(f"Error getting attribute {attribute} from element {locator}: {str(e)}")
            return None
    
    def wait_for_url_contains(self, url_fragment, timeout=None):
        """Wait for URL to contain specific fragment"""
        wait_time = timeout if timeout else self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.url_contains(url_fragment)
            )
            return True
        except TimeoutException:
            logger.error(f"URL does not contain '{url_fragment}' within {wait_time} seconds")
            return False
    
    def wait_for_title_contains(self, title_fragment, timeout=None):
        """Wait for page title to contain specific fragment"""
        wait_time = timeout if timeout else self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.title_contains(title_fragment)
            )
            return True
        except TimeoutException:
            logger.error(f"Title does not contain '{title_fragment}' within {wait_time} seconds")
            return False
    
    def validate_element_text(self, locator, expected_text):
        """Validate element text matches expected value"""
        actual_text = self.get_element_text(locator)
        if actual_text == expected_text:
            logger.info(f"Element text validation passed: '{actual_text}' == '{expected_text}'")
            return True
        else:
            logger.error(f"Element text validation failed: '{actual_text}' != '{expected_text}'")
            return False
    
    def validate_element_attribute(self, locator, attribute, expected_value):
        """Validate element attribute matches expected value"""
        actual_value = self.get_element_attribute(locator, attribute)
        if actual_value == expected_value:
            logger.info(f"Element attribute validation passed: {attribute}='{actual_value}'")
            return True
        else:
            logger.error(f"Element attribute validation failed: {attribute}='{actual_value}' != '{expected_value}'")
            return False
