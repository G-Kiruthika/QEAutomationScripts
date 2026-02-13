# core/driver_factory.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import yaml
import os


def load_config():
    """
    Load configuration from config.yaml file
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def get_driver(browser=None, headless=None):
    """
    Factory method to create and return WebDriver instance
    
    Args:
        browser (str): Browser name ('chrome', 'firefox', 'edge'). Defaults to config value.
        headless (bool): Run browser in headless mode. Defaults to config value.
    
    Returns:
        WebDriver: Selenium WebDriver instance
    """
    config = load_config()
    
    # Use provided values or fall back to config
    browser = browser or config.get('ui', {}).get('browser', 'chrome')
    headless = headless if headless is not None else config.get('ui', {}).get('headless', False)
    
    if browser.lower() == 'chrome':
        chrome_options = ChromeOptions()
        
        # Add options from config
        for option in config.get('selenium', {}).get('chrome_options', []):
            chrome_options.add_argument(option)
        
        if headless:
            chrome_options.add_argument('--headless')
        
        driver = webdriver.Chrome(options=chrome_options)
    
    elif browser.lower() == 'firefox':
        firefox_options = FirefoxOptions()
        
        # Add options from config
        for option in config.get('selenium', {}).get('firefox_options', []):
            firefox_options.add_argument(option)
        
        if headless:
            firefox_options.add_argument('--headless')
        
        driver = webdriver.Firefox(options=firefox_options)
    
    elif browser.lower() == 'edge':
        driver = webdriver.Edge()
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set timeouts from config
    implicit_wait = config.get('ui', {}).get('implicit_wait', 10)
    page_load_timeout = config.get('ui', {}).get('page_load_timeout', 30)
    
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    
    return driver