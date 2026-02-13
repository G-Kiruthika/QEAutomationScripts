# Custom Wait Conditions for Enhanced Synchronization
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

logger = logging.getLogger(__name__)

class CustomWaits:
    """Custom wait conditions for complex UI interactions."""
    
    @staticmethod
    def wait_for_element_visible(driver, locator, timeout=10):
        """Wait for element to be visible."""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.info(f"Element visible: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not visible within {timeout}s: {locator}")
            return None
    
    @staticmethod
    def wait_for_element_clickable(driver, locator, timeout=10):
        """Wait for element to be clickable."""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            logger.info(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not clickable within {timeout}s: {locator}")
            return None
    
    @staticmethod
    def wait_for_url_contains(driver, url_fragment, timeout=10):
        """Wait for URL to contain specific fragment."""
        try:
            WebDriverWait(driver, timeout).until(
                EC.url_contains(url_fragment)
            )
            logger.info(f"URL contains: {url_fragment}")
            return True
        except TimeoutException:
            logger.error(f"URL does not contain '{url_fragment}' within {timeout}s")
            return False
    
    @staticmethod
    def wait_for_text_in_element(driver, locator, text, timeout=10):
        """Wait for specific text to appear in element."""
        try:
            WebDriverWait(driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            logger.info(f"Text '{text}' present in element: {locator}")
            return True
        except TimeoutException:
            logger.error(f"Text '{text}' not present in element within {timeout}s: {locator}")
            return False
