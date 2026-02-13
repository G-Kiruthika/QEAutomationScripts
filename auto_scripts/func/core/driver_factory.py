# core/driver_factory.py
# WebDriver factory for creating and managing browser instances

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import yaml
import os


def load_config():
    """
    Load configuration from config.yaml file
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
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
    Factory method to create and configure WebDriver instance
    
    Args:
        browser (str): Browser type ('chrome', 'firefox', 'edge')
        headless (bool): Run browser in headless mode
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    config = load_config()
    ui_config = config.get('ui', {})
    
    # Use parameters or fall back to config
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
        driver = webdriver.Chrome(options=options)
    
    elif browser.lower() == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
    
    elif browser.lower() == 'edge':
        options = EdgeOptions()
        if headless:
            options.add_argument('--headless')
        driver = webdriver.Edge(options=options)
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Configure timeouts
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    driver.maximize_window()
    
    return driver