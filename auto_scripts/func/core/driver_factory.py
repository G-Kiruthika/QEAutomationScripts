# core/driver_factory.py
from selenium import webdriver

def get_driver():
 # Example: Chrome WebDriver
 options = webdriver.ChromeOptions()
 options.add_argument('--headless')
 driver = webdriver.Chrome(options=options)
 return driver
