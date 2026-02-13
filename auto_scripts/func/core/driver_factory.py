from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import yaml
import os


def load_config():
    """
    Load configuration from config.yaml
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_driver(browser=None, headless=None):
    """
    Factory method to create and return WebDriver instance
    
    Args:
        browser (str): Browser type ('chrome', 'firefox', etc.)
        headless (bool): Run browser in headless mode
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    config = load_config()
    
    if browser is None:
        browser = config.get('browser', {}).get('default', 'chrome')
    
    if headless is None:
        headless = config.get('browser', {}).get('headless', False)
    
    implicit_wait = config.get('browser', {}).get('implicit_wait', 10)
    page_load_timeout = config.get('browser', {}).get('page_load_timeout', 30)
    
    driver = None
    
    if browser.lower() == 'chrome':
        chrome_options = Options()
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
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set timeouts
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    
    return driver
