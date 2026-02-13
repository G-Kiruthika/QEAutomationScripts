"""WebDriver factory for creating and managing browser instances.

Provides centralized driver creation and configuration.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import yaml
import os
from auto_scripts.api.utils.logger import logger


class DriverFactory:
    """Factory class for creating WebDriver instances."""
    
    @staticmethod
    def get_driver(browser=None, headless=None):
        """Create and return WebDriver instance based on configuration.
        
        Args:
            browser (str): Browser type ('chrome', 'firefox', 'edge')
            headless (bool): Run in headless mode
        
        Returns:
            WebDriver: Configured WebDriver instance
        
        Raises:
            ValueError: If unsupported browser specified
        """
        # Load configuration
        config = DriverFactory._load_config()
        
        # Override with parameters if provided
        browser = browser or config.get('browser', 'chrome')
        headless = headless if headless is not None else config.get('headless', False)
        
        logger.info(f"Initializing {browser} driver (headless: {headless})")
        
        if browser.lower() == 'chrome':
            return DriverFactory._create_chrome_driver(headless)
        elif browser.lower() == 'firefox':
            return DriverFactory._create_firefox_driver(headless)
        elif browser.lower() == 'edge':
            return DriverFactory._create_edge_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @staticmethod
    def _load_config():
        """Load configuration from config.yaml.
        
        Returns:
            dict: Configuration dictionary
        """
        try:
            config_path = 'auto_scripts/api/config/config.yaml'
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning("config.yaml not found, using defaults")
            return {'browser': 'chrome', 'headless': False}
    
    @staticmethod
    def _create_chrome_driver(headless=False):
        """Create Chrome WebDriver instance.
        
        Args:
            headless (bool): Run in headless mode
        
        Returns:
            WebDriver: Chrome WebDriver instance
        """
        options = ChromeOptions()
        
        if headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        
        logger.info("Chrome driver created successfully")
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless=False):
        """Create Firefox WebDriver instance.
        
        Args:
            headless (bool): Run in headless mode
        
        Returns:
            WebDriver: Firefox WebDriver instance
        """
        options = FirefoxOptions()
        
        if headless:
            options.add_argument('--headless')
        
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        
        logger.info("Firefox driver created successfully")
        return driver
    
    @staticmethod
    def _create_edge_driver(headless=False):
        """Create Edge WebDriver instance.
        
        Args:
            headless (bool): Run in headless mode
        
        Returns:
            WebDriver: Edge WebDriver instance
        """
        options = EdgeOptions()
        
        if headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Edge(options=options)
        driver.maximize_window()
        
        logger.info("Edge driver created successfully")
        return driver


# Convenience function
def get_driver(browser=None, headless=None):
    """Convenience function to get WebDriver instance.
    
    Args:
        browser (str): Browser type
        headless (bool): Run in headless mode
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    return DriverFactory.get_driver(browser, headless)
