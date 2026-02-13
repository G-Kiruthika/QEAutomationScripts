# core/driver_factory.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import yaml
import os


def get_driver(browser_type=None, headless=None):
    """
    Factory method to create and return a WebDriver instance.
    
    Args:
        browser_type (str): Type of browser ('chrome', 'firefox', 'edge')
        headless (bool): Whether to run browser in headless mode
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Use provided parameters or fall back to config
    browser = browser_type or config['browser']['type']
    is_headless = headless if headless is not None else config['browser']['headless']
    window_size = config['browser'].get('window_size', '1920x1080')
    timeout = config['environment'].get('timeout', 10)
    implicit_wait = config['environment'].get('implicit_wait', 5)
    
    driver = None
    
    if browser.lower() == 'chrome':
        options = webdriver.ChromeOptions()
        if is_headless:
            options.add_argument('--headless')
        options.add_argument(f'--window-size={window_size}')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    
    elif browser.lower() == 'firefox':
        options = webdriver.FirefoxOptions()
        if is_headless:
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    
    elif browser.lower() == 'edge':
        options = webdriver.EdgeOptions()
        if is_headless:
            options.add_argument('--headless')
        options.add_argument(f'--window-size={window_size}')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    
    else:
        raise ValueError(f"Unsupported browser type: {browser}")
    
    # Set timeouts
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(timeout)
    
    # Maximize window if not headless
    if not is_headless:
        driver.maximize_window()
    
    return driver


def quit_driver(driver):
    """
    Safely quit the WebDriver instance.
    
    Args:
        driver: WebDriver instance to quit
    """
    if driver:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error while quitting driver: {str(e)}")
