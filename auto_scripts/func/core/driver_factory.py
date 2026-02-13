"""Driver Factory Module for WebDriver instantiation and management"""

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
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


def get_driver(browser=None, headless=None):
    """Factory method to instantiate WebDriver based on browser type
    
    Args:
        browser (str): Browser type ('chrome', 'firefox', 'edge'). Defaults to config value.
        headless (bool): Run browser in headless mode. Defaults to config value.
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    config = load_config()
    browser_config = config.get('browser', {})
    
    # Set defaults from config or fallback values
    if browser is None:
        browser = browser_config.get('default', 'chrome').lower()
    if headless is None:
        headless = browser_config.get('headless', False)
    
    implicit_wait = browser_config.get('implicit_wait', 10)
    page_load_timeout = browser_config.get('page_load_timeout', 30)
    
    driver = None
    
    if browser == 'chrome':
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        driver = webdriver.Chrome(options=chrome_options)
    
    elif browser == 'firefox':
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)
    
    elif browser == 'edge':
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


def quit_driver(driver):
    """Safely quit the WebDriver instance
    
    Args:
        driver (WebDriver): WebDriver instance to quit
    """
    if driver:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error while quitting driver: {str(e)}")