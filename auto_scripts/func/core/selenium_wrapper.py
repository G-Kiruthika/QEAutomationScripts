from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)
import time
import os


class SeleniumWrapper:
    """Wrapper class for common Selenium operations with enhanced error handling."""
    
    def __init__(self, driver, default_timeout=30):
        self.driver = driver
        self.default_timeout = default_timeout
        self.wait = WebDriverWait(driver, default_timeout)
    
    def find_element(self, locator, timeout=None):
        """Find element with explicit wait."""
        timeout = timeout or self.default_timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not found within {timeout} seconds: {locator}")
    
    def find_elements(self, locator, timeout=None):
        """Find multiple elements with explicit wait."""
        timeout = timeout or self.default_timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present and return it."""
        return self.find_element(locator, timeout)
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible."""
        timeout = timeout or self.default_timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not visible within {timeout} seconds: {locator}")
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable."""
        timeout = timeout or self.default_timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            raise TimeoutException(f"Element not clickable within {timeout} seconds: {locator}")
    
    def click_element(self, locator, timeout=None):
        """Click element with wait and error handling."""
        try:
            element = self.wait_for_element_clickable(locator, timeout)
            element.click()
        except (ElementNotInteractableException, StaleElementReferenceException):
            # Retry with JavaScript click
            element = self.find_element(locator, timeout)
            self.driver.execute_script("arguments[0].click();", element)
    
    def enter_text(self, locator, text, clear_first=True, timeout=None):
        """Enter text into element with wait."""
        element = self.wait_for_element_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_element_text(self, locator, timeout=None):
        """Get text from element."""
        element = self.wait_for_element_visible(locator, timeout)
        return element.text
    
    def get_element_attribute(self, locator, attribute, timeout=None):
        """Get attribute value from element."""
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present in DOM."""
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible."""
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_clickable(self, locator, timeout=5):
        """Check if element is clickable."""
        try:
            self.wait_for_element_clickable(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def select_dropdown_by_text(self, locator, text, timeout=None):
        """Select dropdown option by visible text."""
        element = self.find_element(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(text)
    
    def select_dropdown_by_value(self, locator, value, timeout=None):
        """Select dropdown option by value."""
        element = self.find_element(locator, timeout)
        select = Select(element)
        select.select_by_value(value)
    
    def hover_over_element(self, locator, timeout=None):
        """Hover over element."""
        element = self.find_element(locator, timeout)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element."""
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Small delay for scroll to complete
    
    def take_screenshot(self, filename=None):
        """Take screenshot and save to file."""
        if not filename:
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"
        
        # Create screenshots directory if it doesn't exist
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        
        filepath = os.path.join(screenshots_dir, filename)
        self.driver.save_screenshot(filepath)
        return filepath
    
    def switch_to_frame(self, locator_or_index, timeout=None):
        """Switch to iframe by locator or index."""
        if isinstance(locator_or_index, tuple):
            frame_element = self.find_element(locator_or_index, timeout)
            self.driver.switch_to.frame(frame_element)
        else:
            self.driver.switch_to.frame(locator_or_index)
    
    def switch_to_default_content(self):
        """Switch back to default content from iframe."""
        self.driver.switch_to.default_content()
    
    def switch_to_window(self, window_handle):
        """Switch to specific window."""
        self.driver.switch_to.window(window_handle)
    
    def get_current_url(self):
        """Get current page URL."""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get current page title."""
        return self.driver.title
    
    def refresh_page(self):
        """Refresh current page."""
        self.driver.refresh()
    
    def navigate_back(self):
        """Navigate back in browser history."""
        self.driver.back()
    
    def navigate_forward(self):
        """Navigate forward in browser history."""
        self.driver.forward()
    
    def execute_javascript(self, script, *args):
        """Execute JavaScript code."""
        return self.driver.execute_script(script, *args)
    
    def wait_for_page_load(self, timeout=None):
        """Wait for page to load completely."""
        timeout = timeout or self.default_timeout
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")