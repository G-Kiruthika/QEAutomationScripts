from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options as EdgeOptions
import yaml
import os

def get_driver(browser="chrome", headless=False):
    """
    Factory method to create and return WebDriver instance
    
    Args:
        browser (str): Browser type - 'chrome', 'firefox', 'edge'
        headless (bool): Run browser in headless mode
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            browser = config.get('browser', {}).get('type', browser)
            headless = config.get('browser', {}).get('headless', headless)
    
    driver = None
    
    if browser.lower() == "chrome":
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=chrome_options)
    
    elif browser.lower() == "firefox":
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(options=firefox_options)
    
    elif browser.lower() == "edge":
        edge_options = EdgeOptions()
        if headless:
            edge_options.add_argument("--headless")
        driver = webdriver.Edge(options=edge_options)
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    return driver
