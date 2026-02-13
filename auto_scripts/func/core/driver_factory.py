"""WebDriver Factory Module

Provides centralized WebDriver instantiation and management.
Supports multiple browsers with configurable options.
"""

import os
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import logging

logger = logging.getLogger(__name__)


def load_config():
    """Load configuration from config.yaml file.
    
    Returns:
        dict: Configuration dictionary
    """
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.warning(f"Config file not found at {config_path}. Using defaults.")
        return {}


def get_driver(browser=None, headless=None):
    """Initialize and return a WebDriver instance.
    
    Args:
        browser (str, optional): Browser type ('chrome', 'firefox', 'edge'). 
                                Defaults to config value or 'chrome'.
        headless (bool, optional): Run browser in headless mode. 
                                  Defaults to config value or False.
    
    Returns:
        WebDriver: Configured WebDriver instance
    
    Raises:
        ValueError: If unsupported browser is specified
    """
    config = load_config()
    browser_config = config.get('browser', {})
    
    # Determine browser and headless mode
    browser = browser or browser_config.get('default', 'chrome')
    headless = headless if headless is not None else browser_config.get('headless', False)
    
    logger.info(f"Initializing {browser} driver (headless={headless})")
    
    driver = None
    
    if browser.lower() == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        window_size = browser_config.get('window_size', '1920x1080')
        options.add_argument(f'--window-size={window_size}')
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
    elif browser.lower() == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
    elif browser.lower() == 'edge':
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument('--headless')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set timeouts from config
    implicit_wait = browser_config.get('implicit_wait', 10)
    page_load_timeout = browser_config.get('page_load_timeout', 30)
    
    driver.implicitly_wait(implicit_wait)
    driver.set_page_load_timeout(page_load_timeout)
    
    logger.info(f"{browser.capitalize()} driver initialized successfully")
    return driver


def quit_driver(driver):
    """Safely quit the WebDriver instance.
    
    Args:
        driver (WebDriver): WebDriver instance to quit
    """
    if driver:
        try:
            driver.quit()
            logger.info("Driver quit successfully")
        except Exception as e:
            logger.error(f"Error quitting driver: {str(e)}")
