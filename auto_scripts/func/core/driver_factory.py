from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import yaml
import os

def get_driver(browser_type=None):
    """
    Factory method to create and return WebDriver instance
    
    Args:
        browser_type (str): Type of browser ('chrome', 'firefox', etc.)
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        browser_config = config.get('browser', {})
        browser_type = browser_type or browser_config.get('type', 'chrome')
        headless = browser_config.get('headless', False)
        window_size = browser_config.get('window_size', '1920x1080')
    else:
        browser_type = browser_type or 'chrome'
        headless = False
        window_size = '1920x1080'
    
    if browser_type.lower() == 'chrome':
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument(f'--window-size={window_size}')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
    elif browser_type.lower() == 'firefox':
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    
    # Set implicit wait if configured
    if os.path.exists(config_path):
        implicit_wait = config.get('ui', {}).get('implicit_wait', 5)
        driver.implicitly_wait(implicit_wait)
    
    return driver
