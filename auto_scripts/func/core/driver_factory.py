from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import yaml
import os


def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def get_driver(browser=None, headless=None):
    """Factory method to create and return WebDriver instance
    
    Args:
        browser (str): Browser type ('chrome', 'firefox'). If None, reads from config.
        headless (bool): Run browser in headless mode. If None, reads from config.
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    config = load_config()
    
    if browser is None:
        browser = config.get('ui', {}).get('browser', 'chrome').lower()
    
    if headless is None:
        headless = config.get('ui', {}).get('headless', False)
    
    driver = None
    
    if browser == 'chrome':
        chrome_options = Options()
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
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set implicit wait from config
    implicit_wait = config.get('ui', {}).get('implicit_wait', 10)
    driver.implicitly_wait(implicit_wait)
    
    driver.maximize_window()
    
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
