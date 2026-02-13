# core/driver_factory.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import yaml
import os

def get_driver(browser=None, headless=None):
    """
    Factory method to create and return WebDriver instance
    
    Args:
        browser (str): Browser name (chrome/firefox). If None, reads from config
        headless (bool): Run in headless mode. If None, reads from config
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    browser = browser or config['ui'].get('browser', 'chrome')
    headless = headless if headless is not None else config['ui'].get('headless', False)
    implicit_wait = config['ui'].get('implicit_wait', 10)
    page_load_timeout = config['ui'].get('page_load_timeout', 30)
    
    driver = None
    
    if browser.lower() == 'chrome':
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    elif browser.lower() == 'firefox':
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set timeouts
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    driver.maximize_window()
    
    return driver

def quit_driver(driver):
    """
    Safely quit the WebDriver instance
    
    Args:
        driver: WebDriver instance to quit
    """
    if driver:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error while quitting driver: {str(e)}")
