from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import yaml
import os

def get_driver():
    """
    Factory method to create and return WebDriver instance based on configuration
    Returns: WebDriver instance
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    browser_name = config.get('browser', {}).get('name', 'chrome').lower()
    headless = config.get('browser', {}).get('headless', False)
    window_size = config.get('browser', {}).get('window_size', '1920,1080')
    
    if browser_name == 'chrome':
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument(f'--window-size={window_size}')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        
    elif browser_name == 'firefox':
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument('--headless')
        
        driver = webdriver.Firefox(options=firefox_options)
        
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    # Set implicit wait
    implicit_wait = config.get('environment', {}).get('implicit_wait', 5)
    driver.implicitly_wait(implicit_wait)
    
    return driver