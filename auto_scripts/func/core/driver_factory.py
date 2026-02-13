from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import yaml
import os

def load_config():
    """Load configuration from config.yaml"""
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
    """Factory method to create and return WebDriver instance
    
    Args:
        browser (str): Browser type - 'chrome', 'firefox', 'edge'. Defaults to config value.
        headless (bool): Run browser in headless mode. Defaults to config value.
    
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
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        driver = webdriver.Chrome(options=chrome_options)
    
    elif browser.lower() == 'firefox':
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)
    
    elif browser.lower() == 'edge':
        edge_options = EdgeOptions()
        if headless:
            edge_options.add_argument('--headless')
        driver = webdriver.Edge(options=edge_options)
    
    else:
        raise ValueError(f"Unsupported browser: {browser}. Supported browsers: chrome, firefox, edge")
    
    # Set timeouts
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    
    return driver
