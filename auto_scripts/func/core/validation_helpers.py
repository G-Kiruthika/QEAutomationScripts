from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)


class ValidationHelpers:
    """Enhanced validation helpers for test assertions"""
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible"""
        try:
            wait_time = timeout or self.timeout
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not visible after {wait_time} seconds")
            return None
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable"""
        try:
            wait_time = timeout or self.timeout
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"Element {locator} not clickable after {wait_time} seconds")
            return None
    
    def is_element_present(self, locator):
        """Check if element is present in DOM"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def get_element_text(self, locator):
        """Get text from element"""
        try:
            element = self.wait_for_element_visible(locator)
            return element.text if element else None
        except Exception as e:
            logger.error(f"Failed to get text from element {locator}: {str(e)}")
            return None
    
    def verify_text_in_element(self, locator, expected_text):
        """Verify that element contains expected text"""
        actual_text = self.get_element_text(locator)
        return expected_text in actual_text if actual_text else False
    
    def wait_for_url_contains(self, url_fragment, timeout=None):
        """Wait for URL to contain specific fragment"""
        try:
            wait_time = timeout or self.timeout
            WebDriverWait(self.driver, wait_time).until(
                EC.url_contains(url_fragment)
            )
            return True
        except TimeoutException:
            logger.error(f"URL does not contain '{url_fragment}' after {wait_time} seconds")
            return False
    
    def verify_element_attribute(self, locator, attribute, expected_value):
        """Verify element attribute value"""
        try:
            element = self.wait_for_element_visible(locator)
            if element:
                actual_value = element.get_attribute(attribute)
                return actual_value == expected_value
            return False
        except Exception as e:
            logger.error(f"Failed to verify attribute {attribute} for element {locator}: {str(e)}")
            return False
    
    def count_elements(self, locator):
        """Count number of elements matching locator"""
        try:
            elements = self.driver.find_elements(*locator)
            return len(elements)
        except Exception as e:
            logger.error(f"Failed to count elements {locator}: {str(e)}")
            return 0