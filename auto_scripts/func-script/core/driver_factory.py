from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import yaml
import os


def load_config():
    """Load configuration from config.yaml file"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def get_chrome_driver(headless=False, window_size="1920,1080"):
    """Create and return Chrome WebDriver instance"""
    options = ChromeOptions()
    
    if headless:
        options.add_argument('--headless')
    
    options.add_argument(f'--window-size={window_size}')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver


def get_firefox_driver(headless=False, window_size="1920,1080"):
    """Create and return Firefox WebDriver instance"""
    options = FirefoxOptions()
    
    if headless:
        options.add_argument('--headless')
    
    width, height = window_size.split(',')
    options.add_argument(f'--width={width}')
    options.add_argument(f'--height={height}')
    
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    
    return driver


def get_edge_driver(headless=False, window_size="1920,1080"):
    """Create and return Edge WebDriver instance"""
    options = EdgeOptions()
    
    if headless:
        options.add_argument('--headless')
    
    options.add_argument(f'--window-size={window_size}')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    
    return driver


def get_driver(browser_name=None, headless=None, window_size=None):
    """Factory method to create WebDriver instance based on configuration"""
    config = load_config()
    
    # Use provided parameters or fall back to config
    browser = browser_name or config['browser']['name']
    is_headless = headless if headless is not None else config['browser']['headless']
    size = window_size or config['browser']['window_size']
    
    # Create driver based on browser type
    if browser.lower() == 'chrome':
        driver = get_chrome_driver(is_headless, size)
    elif browser.lower() == 'firefox':
        driver = get_firefox_driver(is_headless, size)
    elif browser.lower() == 'edge':
        driver = get_edge_driver(is_headless, size)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set timeouts from config
    driver.implicitly_wait(config['browser']['implicit_wait'])
    driver.set_page_load_timeout(config['browser']['page_load_timeout'])
    driver.set_script_timeout(config['browser']['script_timeout'])
    
    return driver