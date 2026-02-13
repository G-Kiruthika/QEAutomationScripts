from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class SeleniumWrapper:
    """
    Wrapper class for common Selenium operations
    Provides reusable methods for UI interactions
    """
    
    def __init__(self, driver, timeout=10):
        """
        Initialize SeleniumWrapper
        
        Args:
            driver: Selenium WebDriver instance
            timeout (int): Default timeout for waits
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def wait_for_element(self, locator, timeout=None):
        """
        Wait for element to be present
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Optional custom timeout
        
        Returns:
            WebElement: Found element
        """
        wait_time = timeout if timeout else self.timeout
        wait = WebDriverWait(self.driver, wait_time)
        return wait.until(EC.presence_of_element_located(locator))
    
    def click_element(self, locator):
        """
        Click on element with wait
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator, text):
        """
        Enter text into element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            text (str): Text to enter
        """
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)
    
    def is_element_visible(self, locator, timeout=None):
        """
        Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Optional custom timeout
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            wait_time = timeout if timeout else self.timeout
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def get_text(self, locator):
        """
        Get text from element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        
        Returns:
            str: Element text
        """
        element = self.wait_for_element(locator)
        return element.text
    
    def hover_over_element(self, locator):
        """
        Hover over element
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        """
        element = self.wait_for_element(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
