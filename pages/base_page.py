from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """Base Page Object Model class with common functionality"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)
    
    def wait_for_element(self, locator, timeout=10):
        """Wait for element to be present
        
        Args:
            locator (tuple): Element locator (By.ID, "element_id")
            timeout (int): Maximum wait time in seconds
            
        Returns:
            WebElement: Found element
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_element_clickable(self, locator, timeout=10):
        """Wait for element to be clickable
        
        Args:
            locator (tuple): Element locator
            timeout (int): Maximum wait time in seconds
            
        Returns:
            WebElement: Clickable element
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def click_element(self, locator, timeout=10):
        """Click on element
        
        Args:
            locator (tuple): Element locator
            timeout (int): Maximum wait time in seconds
        """
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()
    
    def enter_text(self, locator, text, timeout=10):
        """Enter text into input field
        
        Args:
            locator (tuple): Element locator
            text (str): Text to enter
            timeout (int): Maximum wait time in seconds
        """
        element = self.wait_for_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator, timeout=10):
        """Get text from element
        
        Args:
            locator (tuple): Element locator
            timeout (int): Maximum wait time in seconds
            
        Returns:
            str: Element text
        """
        element = self.wait_for_element(locator, timeout)
        return element.text
    
    def is_element_visible(self, locator, timeout=5):
        """Check if element is visible
        
        Args:
            locator (tuple): Element locator
            timeout (int): Maximum wait time in seconds
            
        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):
        """Check if element is present in DOM
        
        Args:
            locator (tuple): Element locator
            
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def scroll_to_element(self, locator, timeout=10):
        """Scroll to element
        
        Args:
            locator (tuple): Element locator
            timeout (int): Maximum wait time in seconds
        """
        element = self.wait_for_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def get_current_url(self):
        """Get current page URL
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url
    
    def get_page_title(self):
        """Get page title
        
        Returns:
            str: Page title
        """
        return self.driver.title