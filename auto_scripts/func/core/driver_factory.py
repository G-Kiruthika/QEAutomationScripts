"""Driver Factory Module

Provides WebDriver instantiation and management.
Follows Singleton pattern for driver instances.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import yaml
import os


def get_driver(browser="chrome", headless=False):
    """Get WebDriver instance
    
    Args:
        browser (str): Browser type (chrome, firefox, edge)
        headless (bool): Run browser in headless mode
    
    Returns:
        WebDriver: Selenium WebDriver instance
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            browser = config.get('browser', {}).get('default', browser)
            headless = config.get('browser', {}).get('headless', headless)
    
    if browser.lower() == "chrome":
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    elif browser.lower() == "firefox":
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager
        
        firefox_options = webdriver.FirefoxOptions()
        if headless:
            firefox_options.add_argument("--headless")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    # Set implicit wait and page load timeout
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)
    
    return driver
