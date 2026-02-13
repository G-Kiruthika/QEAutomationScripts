"""WebDriver Factory Module

This module provides factory methods for creating and managing WebDriver instances
for different browsers with appropriate configurations.
"""

import os
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def load_config():
    """Load configuration from config.yaml file.
    
    Returns:
        dict: Configuration dictionary
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as config_file:
            return yaml.safe_load(config_file)
    else:
        # Return default configuration if file doesn't exist
        return {
            'browser': {
                'name': 'chrome',
                'headless': False,
                'implicit_wait': 10,
                'page_load_timeout': 30,
                'window_size': '1920x1080'
            }
        }


def get_driver(browser_name=None, headless=None):
    """Create and configure a WebDriver instance.
    
    Args:
        browser_name (str, optional): Browser name (chrome, firefox, edge). 
                                     Defaults to config value.
        headless (bool, optional): Run browser in headless mode. 
                                  Defaults to config value.
    
    Returns:
        WebDriver: Configured WebDriver instance
    
    Raises:
        ValueError: If unsupported browser is specified
    """
    config = load_config()
    browser_config = config.get('browser', {})
    
    # Use provided values or fall back to config
    browser_name = browser_name or browser_config.get('name', 'chrome')
    headless = headless if headless is not None else browser_config.get('headless', False)
    implicit_wait = browser_config.get('implicit_wait', 10)
    page_load_timeout = browser_config.get('page_load_timeout', 30)
    window_size = browser_config.get('window_size', '1920x1080')
    
    driver = None
    
    if browser_name.lower() == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'--window-size={window_size}')
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
    elif browser_name.lower() == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
    elif browser_name.lower() == 'edge':
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
    else:
        raise ValueError(f"Unsupported browser: {browser_name}. "
                        f"Supported browsers: chrome, firefox, edge")
    
    # Configure timeouts
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    
    # Maximize window if not headless
    if not headless:
        driver.maximize_window()
    
    return driver


def quit_driver(driver):
    """Safely quit the WebDriver instance.
    
    Args:
        driver (WebDriver): WebDriver instance to quit
    """
    if driver:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error while quitting driver: {str(e)}")
