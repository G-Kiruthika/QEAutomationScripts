from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class SeleniumWrapper:
    """Wrapper class for common Selenium WebDriver operations."""
    
    def __init__(self, driver, default_timeout=10):
        """Initialize wrapper with WebDriver instance.
        
        Args:
            driver: WebDriver instance
            default_timeout (int): Default timeout for wait operations
        """
        self.driver = driver
        self.default_timeout = default_timeout
        self.wait = WebDriverWait(driver, default_timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """Wait for element to be present in DOM.
        
        Args:
            locator (tuple): Element locator (By.ID, "element_id")
            timeout (int): Custom timeout, uses default if None
        
        Returns:
            WebElement: Found element
        """
        timeout = timeout or self.default_timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout
        
        Returns:
            WebElement: Visible element
        """
        timeout = timeout or self.default_timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout
        
        Returns:
            WebElement: Clickable element
        """
        timeout = timeout or self.default_timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def click_element(self, locator, timeout=None):
        """Click element after waiting for it to be clickable.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout
        """
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
    
    def enter_text(self, locator, text, clear_first=True, timeout=None):
        """Enter text into element.
        
        Args:
            locator (tuple): Element locator
            text (str): Text to enter
            clear_first (bool): Clear existing text before entering new text
            timeout (int): Custom timeout
        """
        element = self.wait_for_element_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_element_text(self, locator, timeout=None):
        """Get text content of element.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout
        
        Returns:
            str: Element text content
        """
        element = self.wait_for_element_visible(locator, timeout)
        return element.text
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible within timeout.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Timeout for visibility check
        
        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present in DOM within timeout.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Timeout for presence check
        
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def select_dropdown_by_text(self, locator, text, timeout=None):
        """Select dropdown option by visible text.
        
        Args:
            locator (tuple): Dropdown element locator
            text (str): Visible text to select
            timeout (int): Custom timeout
        """
        element = self.wait_for_element_visible(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(text)
    
    def select_dropdown_by_value(self, locator, value, timeout=None):
        """Select dropdown option by value.
        
        Args:
            locator (tuple): Dropdown element locator
            value (str): Value to select
            timeout (int): Custom timeout
        """
        element = self.wait_for_element_visible(locator, timeout)
        select = Select(element)
        select.select_by_value(value)
    
    def hover_over_element(self, locator, timeout=None):
        """Hover over element using ActionChains.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout
        """
        element = self.wait_for_element_visible(locator, timeout)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
    
    def scroll_to_element(self, locator, timeout=None):
        """Scroll to element to bring it into view.
        
        Args:
            locator (tuple): Element locator
            timeout (int): Custom timeout
        """
        element = self.wait_for_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)  # Small delay for scroll to complete
    
    def wait_for_page_load(self, timeout=30):
        """Wait for page to fully load.
        
        Args:
            timeout (int): Timeout for page load
        """
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")