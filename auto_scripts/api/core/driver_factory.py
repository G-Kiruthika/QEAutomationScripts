from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import yaml


def get_driver(browser="chrome", headless=False):
    """
    Factory method to create and return WebDriver instance
    
    Args:
        browser (str): Browser type ('chrome', 'firefox', 'edge')
        headless (bool): Run browser in headless mode
    
    Returns:
        WebDriver: Configured WebDriver instance
    """
    # Load configuration
    try:
        with open('auto_scripts/api/config/config.yaml') as f:
            config = yaml.safe_load(f)
            base_url = config.get('ui', {}).get('base_url', 'http://localhost:8080')
    except FileNotFoundError:
        base_url = 'http://localhost:8080'
    
    driver = None
    
    if browser.lower() == "chrome":
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)
    
    elif browser.lower() == "firefox":
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(options=firefox_options)
    
    elif browser.lower() == "edge":
        driver = webdriver.Edge()
    
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    driver.implicitly_wait(10)
    driver.get(base_url)
    
    return driver
