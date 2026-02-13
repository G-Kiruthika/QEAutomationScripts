from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base Page Object class with common methods for all page objects"""
    
    def __init__(self, driver, timeout=10):
        """
        Initialize BasePage
        
        Args:
            driver: Selenium WebDriver instance
            timeout (int): Default timeout for waits
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def find_element(self, locator):
        """
        Find element with explicit wait
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        
        Returns:
            WebElement: Found element
        """
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        """
        Find multiple elements
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        
        Returns:
            list: List of WebElements
        """
        return self.driver.find_elements(*locator)
    
    def is_visible(self, locator):
        """
        Check if element is visible
        
        Args:
            locator (tuple): Locator tuple (By.TYPE, "value")
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def click_element(self, locator):
        """
        Click on element
        
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
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
