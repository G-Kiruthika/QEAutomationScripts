"""Base Page class with common UI automation methods"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def find_element(self, locator):
        """Find element with explicit wait"""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise
    
    def click_element(self, locator):
        """Click on element"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            logger.info(f"Clicked element: {locator}")
        except Exception as e:
            logger.error(f"Failed to click element {locator}: {str(e)}")
            raise
    
    def enter_text(self, locator, text):
        """Enter text into input field"""
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
            logger.info(f"Entered text into element: {locator}")
        except Exception as e:
            logger.error(f"Failed to enter text into {locator}: {str(e)}")
            raise
    
    def get_element_text(self, locator):
        """Get text from element"""
        try:
            element = self.find_element(locator)
            text = element.text
            logger.info(f"Retrieved text from element: {locator}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from {locator}: {str(e)}")
            raise
    
    def is_element_visible(self, locator):
        """Check if element is visible"""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except TimeoutException:
            logger.warning(f"Element not visible: {locator}")
            return False
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present"""
        wait_time = timeout if timeout else self.timeout
        try:
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            logger.error(f"Element not found within {wait_time} seconds: {locator}")
            raise
    
    def navigate_to(self, url):
        """Navigate to URL"""
        try:
            self.driver.get(url)
            logger.info(f"Navigated to: {url}")
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {str(e)}")
            raise
