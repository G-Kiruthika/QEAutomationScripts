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
 """
 Load configuration from config.yaml file.
 
 Returns:
 dict: Configuration dictionary
 """
 config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
 
 try:
 with open(config_path, 'r') as f:
 config = yaml.safe_load(f)
 return config
 except FileNotFoundError:
 # Return default config if file not found
 return {
 'browser': {
 'type': 'chrome',
 'headless': False,
 'implicit_wait': 10,
 'page_load_timeout': 30,
 'window_size': '1920x1080'
 }
 }


def get_driver(browser_type=None, headless=None):
 """
 Factory method to create and configure WebDriver instance.
 
 Args:
 browser_type (str, optional): Browser type (chrome, firefox, edge). Defaults to config value.
 headless (bool, optional): Run browser in headless mode. Defaults to config value.
 
 Returns:
 WebDriver: Configured WebDriver instance
 """
 config = load_config()
 browser_config = config.get('browser', {})
 
 # Use parameters or fall back to config
 browser = browser_type or browser_config.get('type', 'chrome')
 is_headless = headless if headless is not None else browser_config.get('headless', False)
 implicit_wait = browser_config.get('implicit_wait', 10)
 page_load_timeout = browser_config.get('page_load_timeout', 30)
 window_size = browser_config.get('window_size', '1920x1080')
 
 driver = None
 
 if browser.lower() == 'chrome':
 options = ChromeOptions()
 if is_headless:
 options.add_argument('--headless')
 options.add_argument('--no-sandbox')
 options.add_argument('--disable-dev-shm-usage')
 options.add_argument(f'--window-size={window_size}')
 driver = webdriver.Chrome(options=options)
 
 elif browser.lower() == 'firefox':
 options = FirefoxOptions()
 if is_headless:
 options.add_argument('--headless')
 driver = webdriver.Firefox(options=options)
 
 elif browser.lower() == 'edge':
 options = EdgeOptions()
 if is_headless:
 options.add_argument('--headless')
 driver = webdriver.Edge(options=options)
 
 else:
 raise ValueError(f"Unsupported browser type: {browser}")
 
 # Configure timeouts
 driver.implicitly_wait(implicit_wait)
 driver.set_page_load_timeout(page_load_timeout)
 
 # Maximize window if not headless
 if not is_headless:
 driver.maximize_window()
 
 return driver


def get_remote_driver(hub_url, browser_type='chrome', headless=False):
 """
 Create a remote WebDriver instance for Selenium Grid.
 
 Args:
 hub_url (str): Selenium Grid hub URL
 browser_type (str): Browser type (chrome, firefox, edge)
 headless (bool): Run browser in headless mode
 
 Returns:
 WebDriver: Remote WebDriver instance
 """
 if browser_type.lower() == 'chrome':
 options = ChromeOptions()
 if headless:
 options.add_argument('--headless')
 options.add_argument('--no-sandbox')
 options.add_argument('--disable-dev-shm-usage')
 elif browser_type.lower() == 'firefox':
 options = FirefoxOptions()
 if headless:
 options.add_argument('--headless')
 elif browser_type.lower() == 'edge':
 options = EdgeOptions()
 if headless:
 options.add_argument('--headless')
 else:
 raise ValueError(f"Unsupported browser type: {browser_type}")
 
 driver = webdriver.Remote(command_executor=hub_url, options=options)
 driver.implicitly_wait(10)
 driver.maximize_window()
 
 return driver