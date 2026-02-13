# core/selenium_wrapper.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException
)
from selenium.webdriver.common.action_chains import ActionChains
import time


class SeleniumWrapper:
    """
    Wrapper class for common Selenium operations with enhanced error handling and waits.
    """
    
    def __init__(self, driver, timeout=10):
        """
        Initialize the wrapper with a WebDriver instance.
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout for waits in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """
        Wait for an element to be present in the DOM.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout, uses default if not provided
        
        Returns:
            WebElement: The found element
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        try:
            element = wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not found within {wait_time} seconds")
    
    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for an element to be visible.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout
        
        Returns:
            WebElement: The visible element
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        try:
            element = wait.until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not visible within {wait_time} seconds")
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for an element to be clickable.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout
        
        Returns:
            WebElement: The clickable element
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        try:
            element = wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not clickable within {wait_time} seconds")
    
    def click_element(self, locator, timeout=None):
        """
        Click an element with wait and retry logic.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout
        """
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                element = self.wait_for_element_clickable(locator, timeout)
                element.click()
                return
            except (StaleElementReferenceException, ElementNotInteractableException) as e:
                if attempt == max_attempts - 1:
                    raise
                time.sleep(0.5)
    
    def enter_text(self, locator, text, clear_first=True, timeout=None):
        """
        Enter text into an input field.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            text (str): Text to enter
            clear_first (bool): Whether to clear the field first
            timeout (int): Custom timeout
        """
        element = self.wait_for_element_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, timeout=None):
        """
        Get text from an element.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout
        
        Returns:
            str: Element text
        """
        element = self.wait_for_element_visible(locator, timeout)
        return element.text
    
    def is_element_visible(self, locator, timeout=2):
        """
        Check if an element is visible.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Timeout for check
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def is_element_present(self, locator, timeout=2):
        """
        Check if an element is present in DOM.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Timeout for check
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.wait_for_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def scroll_to_element(self, locator, timeout=None):
        """
        Scroll to an element.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout
        """
        element = self.wait_for_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)  # Small delay for smooth scrolling
    
    def hover_over_element(self, locator, timeout=None):
        """
        Hover over an element.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout
        """
        element = self.wait_for_element_visible(locator, timeout)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
    
    def get_attribute(self, locator, attribute_name, timeout=None):
        """
        Get an attribute value from an element.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            attribute_name (str): Name of the attribute
            timeout (int): Custom timeout
        
        Returns:
            str: Attribute value
        """
        element = self.wait_for_element(locator, timeout)
        return element.get_attribute(attribute_name)
    
    def wait_for_url_contains(self, url_fragment, timeout=None):
        """
        Wait for URL to contain a specific fragment.
        
        Args:
            url_fragment (str): URL fragment to wait for
            timeout (int): Custom timeout
        
        Returns:
            bool: True if URL contains fragment
        """
        wait_time = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        try:
            return wait.until(EC.url_contains(url_fragment))
        except TimeoutException:
            raise TimeoutException(f"URL did not contain '{url_fragment}' within {wait_time} seconds")
    
    def switch_to_frame(self, locator, timeout=None):
        """
        Switch to an iframe.
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, 'value')
            timeout (int): Custom timeout
        """
        element = self.wait_for_element(locator, timeout)
        self.driver.switch_to.frame(element)
    
    def switch_to_default_content(self):
        """
        Switch back to default content from iframe.
        """
        self.driver.switch_to.default_content()
