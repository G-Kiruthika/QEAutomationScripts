# Driver Factory for WebDriver instantiation
# Supports multiple browsers and configurations

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import yaml
import os


def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_driver(browser=None, headless=None):
    """Get WebDriver instance based on configuration
    
    Args:
        browser (str): Browser type ('chrome', 'firefox'). Defaults to config value.
        headless (bool): Run in headless mode. Defaults to config value.
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    config = load_config()
    
    if browser is None:
        browser = config['ui'].get('browser', 'chrome').lower()
    
    if headless is None:
        headless = config['ui'].get('headless', False)
    
    if browser == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Chrome(options=options)
    
    elif browser == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        
        driver = webdriver.Firefox(options=options)
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set timeouts from config
    driver.implicitly_wait(config['ui'].get('implicit_wait', 10))
    driver.set_page_load_timeout(config['ui'].get('page_load_timeout', 30))
    
    return driver
