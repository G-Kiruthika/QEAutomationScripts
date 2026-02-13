"""WebDriver factory module for creating and managing browser instances.

This module provides a centralized way to instantiate WebDriver instances
with proper configuration and options.
"""

import os
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
import yaml


def load_config():
    """
    Load configuration from config.yaml file.
    
    Returns:
        dict: Configuration dictionary
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # Return default config if file not found
        return {
            'ui': {
                'browser': 'chrome',
                'headless': False,
                'implicit_wait': 10,
                'page_load_timeout': 30
            }
        }


def get_driver(browser=None, headless=None):
    """
    Create and return a WebDriver instance based on configuration.
    
    Args:
        browser (str, optional): Browser type ('chrome', 'firefox', 'edge'). 
                                Defaults to config value.
        headless (bool, optional): Run browser in headless mode. 
                                  Defaults to config value.
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    config = load_config()
    ui_config = config.get('ui', {})
    
    # Use provided values or fall back to config
    browser = browser or ui_config.get('browser', 'chrome')
    headless = headless if headless is not None else ui_config.get('headless', False)
    implicit_wait = ui_config.get('implicit_wait', 10)
    page_load_timeout = ui_config.get('page_load_timeout', 30)
    
    driver = None
    
    if browser.lower() == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    
    elif browser.lower() == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    
    elif browser.lower() == 'edge':
        options = EdgeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set timeouts
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    
    return driver


def quit_driver(driver):
    """
    Safely quit the WebDriver instance.
    
    Args:
        driver (WebDriver): WebDriver instance to quit
    """
    if driver:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error while quitting driver: {str(e)}")