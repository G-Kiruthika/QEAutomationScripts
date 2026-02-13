from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

class SeleniumWrapper:
    """
    Wrapper class providing enhanced Selenium operations with explicit waits
    and error handling
    """
    
    def __init__(self, driver, timeout=10):
        """
        Initialize SeleniumWrapper
        
        Args:
            driver: WebDriver instance
            timeout (int): Default timeout for waits in seconds
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """
        Wait for element to be present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        
        Returns:
            WebElement: Found element
        """
        wait_time = timeout if timeout else self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for element to be visible
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        
        Returns:
            WebElement: Visible element
        """
        wait_time = timeout if timeout else self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for element to be clickable
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        
        Returns:
            WebElement: Clickable element
        """
        wait_time = timeout if timeout else self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def click_element(self, locator, timeout=None):
        """
        Wait for element and click it
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        """
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
    
    def enter_text(self, locator, text, timeout=None, clear_first=True):
        """
        Wait for element and enter text
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            text (str): Text to enter
            timeout (int): Custom timeout, uses default if None
            clear_first (bool): Clear field before entering text
        """
        element = self.wait_for_element_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, timeout=None):
        """
        Wait for element and get its text
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        
        Returns:
            str: Element text
        """
        element = self.wait_for_element_visible(locator, timeout)
        return element.text
    
    def is_element_visible(self, locator, timeout=None):
        """
        Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            self.wait_for_element_visible(locator, timeout if timeout else 5)
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator, timeout=None):
        """
        Check if element is present in DOM
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        
        Returns:
            bool: True if present, False otherwise
        """
        try:
            self.wait_for_element(locator, timeout if timeout else 5)
            return True
        except TimeoutException:
            return False
    
    def scroll_to_element(self, locator, timeout=None):
        """
        Scroll to element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        """
        element = self.wait_for_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def hover_over_element(self, locator, timeout=None):
        """
        Hover over element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Custom timeout, uses default if None
        """
        element = self.wait_for_element_visible(locator, timeout)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
    
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
        element = self.wait_for_element(locator, timeout)
        return element.get_attribute(attribute)
