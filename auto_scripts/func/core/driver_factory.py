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
    """Load configuration from config.yaml file."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        # Return default config if file not found
        return {
            'browser': {
                'default': 'chrome',
                'headless': False,
                'window_size': '1920,1080',
                'implicit_wait': 10,
                'explicit_wait': 30,
                'page_load_timeout': 30
            }
        }


def get_driver(browser_name=None, headless=None):
    """Factory method to create and return WebDriver instance."""
    config = load_config()
    browser_config = config.get('browser', {})
    
    # Use provided browser or default from config
    browser = browser_name or browser_config.get('default', 'chrome')
    is_headless = headless if headless is not None else browser_config.get('headless', False)
    
    driver = None
    
    if browser.lower() == 'chrome':
        driver = _create_chrome_driver(config, is_headless)
    elif browser.lower() == 'firefox':
        driver = _create_firefox_driver(config, is_headless)
    elif browser.lower() == 'edge':
        driver = _create_edge_driver(config, is_headless)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Configure driver timeouts
    if driver:
        driver.implicitly_wait(browser_config.get('implicit_wait', 10))
        driver.set_page_load_timeout(browser_config.get('page_load_timeout', 30))
        
        # Set window size
        window_size = browser_config.get('window_size', '1920,1080')
        width, height = map(int, window_size.split(','))
        driver.set_window_size(width, height)
    
    return driver


def _create_chrome_driver(config, headless):
    """Create Chrome WebDriver instance."""
    options = ChromeOptions()
    
    if headless:
        options.add_argument('--headless')
    
    # Add default Chrome options
    webdriver_config = config.get('webdriver', {}).get('chrome', {})
    chrome_options = webdriver_config.get('options', [])
    
    for option in chrome_options:
        options.add_argument(option)
    
    # Additional stability options
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        raise Exception(f"Failed to create Chrome driver: {str(e)}")


def _create_firefox_driver(config, headless):
    """Create Firefox WebDriver instance."""
    options = FirefoxOptions()
    
    if headless:
        options.add_argument('--headless')
    
    # Add Firefox options from config
    webdriver_config = config.get('webdriver', {}).get('firefox', {})
    firefox_options = webdriver_config.get('options', [])
    
    for option in firefox_options:
        options.add_argument(option)
    
    try:
        return webdriver.Firefox(options=options)
    except Exception as e:
        raise Exception(f"Failed to create Firefox driver: {str(e)}")


def _create_edge_driver(config, headless):
    """Create Edge WebDriver instance."""
    options = EdgeOptions()
    
    if headless:
        options.add_argument('--headless')
    
    # Add Edge options from config
    webdriver_config = config.get('webdriver', {}).get('edge', {})
    edge_options = webdriver_config.get('options', [])
    
    for option in edge_options:
        options.add_argument(option)
    
    try:
        return webdriver.Edge(options=options)
    except Exception as e:
        raise Exception(f"Failed to create Edge driver: {str(e)}")


def quit_driver(driver):
    """Safely quit the WebDriver instance."""
    if driver:
        try:
            driver.quit()
        except Exception as e:
            print(f"Error while quitting driver: {str(e)}")