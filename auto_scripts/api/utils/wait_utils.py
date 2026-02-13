from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class WaitUtils:
    """
    Utility class for custom wait conditions and helpers
    """
    
    @staticmethod
    def wait_for_element_visible(driver, locator, timeout=10):
        """
        Wait for element to be visible
        
        Args:
            driver: WebDriver instance
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Timeout in seconds
        
        Returns:
            WebElement: Visible element
        
        Raises:
            TimeoutException: If element not visible within timeout
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    @staticmethod
    def wait_for_element_clickable(driver, locator, timeout=10):
        """
        Wait for element to be clickable
        
        Args:
            driver: WebDriver instance
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Timeout in seconds
        
        Returns:
            WebElement: Clickable element
        
        Raises:
            TimeoutException: If element not clickable within timeout
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    @staticmethod
    def wait_for_element_present(driver, locator, timeout=10):
        """
        Wait for element to be present in DOM
        
        Args:
            driver: WebDriver instance
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Timeout in seconds
        
        Returns:
            WebElement: Present element
        
        Raises:
            TimeoutException: If element not present within timeout
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    @staticmethod
    def wait_for_text_in_element(driver, locator, text, timeout=10):
        """
        Wait for specific text to appear in element
        
        Args:
            driver: WebDriver instance
            locator (tuple): Locator tuple (By.TYPE, "value")
            text (str): Expected text
            timeout (int): Timeout in seconds
        
        Returns:
            bool: True if text found
        
        Raises:
            TimeoutException: If text not found within timeout
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, text))
    
    @staticmethod
    def wait_for_url_contains(driver, url_fragment, timeout=10):
        """
        Wait for URL to contain specific fragment
        
        Args:
            driver: WebDriver instance
            url_fragment (str): URL fragment to wait for
            timeout (int): Timeout in seconds
        
        Returns:
            bool: True if URL contains fragment
        
        Raises:
            TimeoutException: If URL doesn't contain fragment within timeout
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.url_contains(url_fragment))
    
    @staticmethod
    def is_element_visible(driver, locator, timeout=5):
        """
        Check if element is visible (non-throwing version)
        
        Args:
            driver: WebDriver instance
            locator (tuple): Locator tuple (By.TYPE, "value")
            timeout (int): Timeout in seconds
        
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            WaitUtils.wait_for_element_visible(driver, locator, timeout)
            return True
        except TimeoutException:
            return False
