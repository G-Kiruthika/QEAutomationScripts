"""Driver Factory Module

This module provides factory methods for creating and managing WebDriver instances.
Supports multiple browsers and configuration options.
"""

import os
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class DriverFactory:
    """Factory class for creating WebDriver instances"""

    @staticmethod
    def _load_config():
        """Load configuration from config.yaml file
        
        Returns:
            dict: Configuration dictionary
        """
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            # Return default configuration if file not found
            return {
                'browser': {
                    'type': 'chrome',
                    'headless': False,
                    'implicit_wait': 10,
                    'page_load_timeout': 30,
                    'window_size': 'maximize'
                }
            }

    @staticmethod
    def _get_chrome_driver(headless=False):
        """Create and configure Chrome WebDriver
        
        Args:
            headless (bool): Whether to run browser in headless mode
            
        Returns:
            WebDriver: Configured Chrome WebDriver instance
        """
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    @staticmethod
    def _get_firefox_driver(headless=False):
        """Create and configure Firefox WebDriver
        
        Args:
            headless (bool): Whether to run browser in headless mode
            
        Returns:
            WebDriver: Configured Firefox WebDriver instance
        """
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        return driver

    @staticmethod
    def _get_edge_driver(headless=False):
        """Create and configure Edge WebDriver
        
        Args:
            headless (bool): Whether to run browser in headless mode
            
        Returns:
            WebDriver: Configured Edge WebDriver instance
        """
        options = EdgeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        return driver

    @staticmethod
    def create_driver(browser_type=None, headless=None):
        """Create WebDriver instance based on browser type
        
        Args:
            browser_type (str, optional): Type of browser (chrome, firefox, edge)
            headless (bool, optional): Whether to run in headless mode
            
        Returns:
            WebDriver: Configured WebDriver instance
            
        Raises:
            ValueError: If unsupported browser type is specified
        """
        config = DriverFactory._load_config()
        browser_config = config.get('browser', {})
        
        # Use provided values or fall back to config
        browser_type = browser_type or browser_config.get('type', 'chrome')
        headless = headless if headless is not None else browser_config.get('headless', False)
        
        # Create driver based on browser type
        if browser_type.lower() == 'chrome':
            driver = DriverFactory._get_chrome_driver(headless)
        elif browser_type.lower() == 'firefox':
            driver = DriverFactory._get_firefox_driver(headless)
        elif browser_type.lower() == 'edge':
            driver = DriverFactory._get_edge_driver(headless)
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        
        # Apply configuration settings
        implicit_wait = browser_config.get('implicit_wait', 10)
        page_load_timeout = browser_config.get('page_load_timeout', 30)
        window_size = browser_config.get('window_size', 'maximize')
        
        driver.implicitly_wait(implicit_wait)
        driver.set_page_load_timeout(page_load_timeout)
        
        if window_size == 'maximize':
            driver.maximize_window()
        elif window_size == 'fullscreen':
            driver.fullscreen_window()
        elif ',' in str(window_size):
            width, height = map(int, window_size.split(','))
            driver.set_window_size(width, height)
        
        return driver


def get_driver(browser_type=None, headless=None):
    """Convenience function to get a WebDriver instance
    
    Args:
        browser_type (str, optional): Type of browser (chrome, firefox, edge)
        headless (bool, optional): Whether to run in headless mode
        
    Returns:
        WebDriver: Configured WebDriver instance
    """
    return DriverFactory.create_driver(browser_type, headless)
