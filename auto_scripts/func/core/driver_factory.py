"""WebDriver Factory Module

Provides centralized WebDriver instantiation and management.
Supports multiple browsers with configurable options.
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
    try:
        with open(config_path, 'r') as config_file:
            return yaml.safe_load(config_file)
    except FileNotFoundError:
        # Return default configuration if file not found
        return {
            'browser': {'type': 'chrome', 'headless': False, 'window_size': '1920x1080'},
            'app': {'timeout': 30, 'implicit_wait': 10}
        }


def get_driver(browser_type=None, headless=None):
    """Create and return a WebDriver instance.
    
    Args:
        browser_type (str, optional): Browser type (chrome, firefox, edge). 
                                     Defaults to config value.
        headless (bool, optional): Run browser in headless mode. 
                                  Defaults to config value.
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    config = load_config()
    
    # Use provided values or fall back to config
    browser_type = browser_type or config.get('browser', {}).get('type', 'chrome')
    headless = headless if headless is not None else config.get('browser', {}).get('headless', False)
    window_size = config.get('browser', {}).get('window_size', '1920x1080')
    implicit_wait = config.get('app', {}).get('implicit_wait', 10)
    
    driver = None
    
    if browser_type.lower() == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument(f'--window-size={window_size}')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
    elif browser_type.lower() == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
    elif browser_type.lower() == 'edge':
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument(f'--window-size={window_size}')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    
    # Set implicit wait
    driver.implicitly_wait(implicit_wait)
    
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
