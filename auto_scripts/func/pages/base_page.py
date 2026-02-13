from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from core.selenium_wrapper import SeleniumWrapper

class BasePage:
    """
    Base Page class that all page objects inherit from.
    Provides common functionality for all pages.
    """
    
    def __init__(self, driver, timeout=10):
        """
        Initialize BasePage
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout for waits
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.wrapper = SeleniumWrapper(driver, timeout)
    
    def find_element(self, locator, timeout=None):
        """
        Find element with explicit wait
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        
        Returns:
            WebElement: Found element
        """
        return self.wrapper.wait_for_element(locator, timeout)
    
    def find_elements(self, locator, timeout=None):
        """
        Find multiple elements with explicit wait
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        
        Returns:
            list: List of WebElements
        """
        wait_time = timeout if timeout else self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)
    
    def click_element(self, locator, timeout=None):
        """
        Click element with explicit wait
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        """
        self.wrapper.click_element(locator, timeout)
    
    def enter_text(self, locator, text, timeout=None, clear_first=True):
        """
        Enter text into element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            text (str): Text to enter
            timeout (int): Custom timeout, uses default if None
            clear_first (bool): Clear field before entering text
        """
        self.wrapper.enter_text(locator, text, timeout, clear_first)
    
    def get_text(self, locator, timeout=None):
        """
        Get element text
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        
        Returns:
            str: Element text
        """
        return self.wrapper.get_text(locator, timeout)
    
    def is_element_visible(self, locator, timeout=None):
        """
        Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        
        Returns:
            bool: True if visible, False otherwise
        """
        return self.wrapper.is_element_visible(locator, timeout)
    
    def is_element_present(self, locator, timeout=None):
        """
        Check if element is present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        
        Returns:
            bool: True if present, False otherwise
        """
        return self.wrapper.is_element_present(locator, timeout)
    
    def navigate_to(self, url):
        """
        Navigate to URL
        
        Args:
            url (str): URL to navigate to
        """
        self.driver.get(url)
    
    def get_current_url(self):
        """
        Get current page URL
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url
    
    def get_page_title(self):
        """
        Get page title
        
        Returns:
            str: Page title
        """
        return self.driver.title
    
    def refresh_page(self):
        """
        Refresh current page
        """
        self.driver.refresh()
    
    def scroll_to_element(self, locator, timeout=None):
        """
        Scroll to element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        """
        self.wrapper.scroll_to_element(locator, timeout)
    
    def get_attribute(self, locator, attribute, timeout=None):
        """
        Get element attribute value
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            attribute (str): Attribute name
            timeout (int): Custom timeout, uses default if None
        
        Returns:
            str: Attribute value
        """
        return self.wrapper.get_attribute(locator, attribute, timeout)
