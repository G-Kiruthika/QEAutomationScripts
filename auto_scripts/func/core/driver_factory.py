from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import yaml
import os

def get_driver(browser="chrome", headless=False):
    """Get WebDriver instance based on browser type and configuration.
    
    Args:
        browser (str): Browser type ('chrome', 'firefox')
        headless (bool): Run browser in headless mode
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        browser_config = config.get('ui', {}).get('browser', {})
    except FileNotFoundError:
        browser_config = {}
    
    if browser.lower() == "chrome":
        chrome_options = Options()
        if headless or browser_config.get('headless', False):
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Add additional options from config
        additional_options = browser_config.get('chrome_options', [])
        for option in additional_options:
            chrome_options.add_argument(option)
        
        driver = webdriver.Chrome(options=chrome_options)
        
    elif browser.lower() == "firefox":
        firefox_options = FirefoxOptions()
        if headless or browser_config.get('headless', False):
            firefox_options.add_argument("--headless")
        
        # Add additional options from config
        additional_options = browser_config.get('firefox_options', [])
        for option in additional_options:
            firefox_options.add_argument(option)
        
        driver = webdriver.Firefox(options=firefox_options)
        
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set implicit wait
    driver.implicitly_wait(browser_config.get('implicit_wait', 10))
    
    # Maximize window if not headless
    if not (headless or browser_config.get('headless', False)):
        driver.maximize_window()
    
    return driver