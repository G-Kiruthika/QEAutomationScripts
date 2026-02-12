# core/driver_factory.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import yaml
import os


def get_driver(browser="chrome", headless=False):
 """
 Factory method to create and return a WebDriver instance.
 
 Args:
 browser (str): Browser type - 'chrome', 'firefox', 'edge'
 headless (bool): Run browser in headless mode
 
 Returns:
 WebDriver: Configured WebDriver instance
 """
 # Load configuration
 config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
 config = {}
 if os.path.exists(config_path):
 with open(config_path, 'r') as f:
 config = yaml.safe_load(f) or {}
 
 browser = browser.lower()
 
 if browser == "chrome":
 chrome_options = Options()
 if headless:
 chrome_options.add_argument("--headless")
 chrome_options.add_argument("--no-sandbox")
 chrome_options.add_argument("--disable-dev-shm-usage")
 chrome_options.add_argument("--disable-gpu")
 chrome_options.add_argument("--window-size=1920,1080")
 
 driver = webdriver.Chrome(options=chrome_options)
 
 elif browser == "firefox":
 firefox_options = FirefoxOptions()
 if headless:
 firefox_options.add_argument("--headless")
 firefox_options.add_argument("--width=1920")
 firefox_options.add_argument("--height=1080")
 
 driver = webdriver.Firefox(options=firefox_options)
 
 elif browser == "edge":
 edge_options = webdriver.EdgeOptions()
 if headless:
 edge_options.add_argument("--headless")
 edge_options.add_argument("--no-sandbox")
 edge_options.add_argument("--disable-dev-shm-usage")
 
 driver = webdriver.Edge(options=edge_options)
 
 else:
 raise ValueError(f"Unsupported browser: {browser}. Supported browsers: chrome, firefox, edge")
 
 # Set implicit wait
 driver.implicitly_wait(10)
 driver.maximize_window()
 
 return driver
