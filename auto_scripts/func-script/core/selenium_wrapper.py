from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)
import time
import logging


class SeleniumWrapper:
    """Wrapper class for common Selenium operations with enhanced error handling and waits"""
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.logger = logging.getLogger(__name__)
    
    def find_element(self, locator, timeout=None):
        """Find element with explicit wait"""
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found with locator: {locator}")
            raise
    
    def find_elements(self, locator, timeout=None):
        """Find multiple elements with explicit wait"""
        wait_time = timeout or self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            self.logger.error(f"Elements not found with locator: {locator}")
            return []
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible"""
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible with locator: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable"""
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not clickable with locator: {locator}")
            raise
    
    def click_element(self, locator, timeout=None):
        """Click element with retry mechanism"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                element = self.wait_for_element_clickable(locator, timeout)
                element.click()
                return
            except (StaleElementReferenceException, ElementNotInteractableException) as e:
                if attempt == max_attempts - 1:
                    self.logger.error(f"Failed to click element after {max_attempts} attempts: {locator}")
                    raise
                time.sleep(0.5)
    
    def enter_text(self, locator, text, clear_first=True, timeout=None):
        """Enter text into input field"""
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if clear_first:
                element.clear()
            element.send_keys(text)
        except Exception as e:
            self.logger.error(f"Failed to enter text '{text}' into element {locator}: {str(e)}")
            raise
    
    def get_text(self, locator, timeout=None):
        """Get text from element"""
        try:
            element = self.wait_for_element_visible(locator, timeout)
            return element.text
        except Exception as e:
            self.logger.error(f"Failed to get text from element {locator}: {str(e)}")
            raise
    
    def get_attribute(self, locator, attribute_name, timeout=None):
        """Get attribute value from element"""
        try:
            element = self.find_element(locator, timeout)
            return element.get_attribute(attribute_name)
        except Exception as e:
            self.logger.error(f"Failed to get attribute '{attribute_name}' from element {locator}: {str(e)}")
            raise
    
    def is_element_visible(self, locator, timeout=2):
        """Check if element is visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=2):
        """Check if element is present in DOM"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_text_in_element(self, locator, text, timeout=None):
        """Wait for specific text to appear in element"""
        wait_time = timeout or self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            return True
        except TimeoutException:
            self.logger.error(f"Text '{text}' not found in element {locator}")
            return False
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element"""
        try:
            element = self.find_element(locator, timeout)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Allow time for scroll to complete
        except Exception as e:
            self.logger.error(f"Failed to scroll to element {locator}: {str(e)}")
            raise
    
    def hover_over_element(self, locator, timeout=None):
        """Hover over element"""
        try:
            element = self.wait_for_element_visible(locator, timeout)
            ActionChains(self.driver).move_to_element(element).perform()
        except Exception as e:
            self.logger.error(f"Failed to hover over element {locator}: {str(e)}")
            raise
    
    def select_dropdown_by_text(self, locator, text, timeout=None):
        """Select dropdown option by visible text"""
        from selenium.webdriver.support.ui import Select
        try:
            element = self.find_element(locator, timeout)
            select = Select(element)
            select.select_by_visible_text(text)
        except Exception as e:
            self.logger.error(f"Failed to select dropdown option '{text}' from {locator}: {str(e)}")
            raise
    
    def take_screenshot(self, filename):
        """Take screenshot and save to file"""
        try:
            self.driver.save_screenshot(filename)
            self.logger.info(f"Screenshot saved: {filename}")
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            raise