from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

USERNAME = 'valid_user@example.com'
PASSWORD = 'ValidPassword123'
LOGIN_URL = 'https://example-ecommerce.com/login'

with webdriver.Chrome() as driver:
    driver.get(LOGIN_URL)
    driver.find_element(By.ID, 'username').send_keys(USERNAME)
    driver.find_element(By.ID, 'password').send_keys(PASSWORD)
    driver.find_element(By.ID, 'login-button').click()
    time.sleep(2)
    assert driver.current_url == 'https://example-ecommerce.com/dashboard', 'Did not redirect to dashboard.'
    assert driver.get_cookie('session_token'), 'Session token not generated.'
    error_elements = driver.find_elements(By.CLASS_NAME, 'error-message')
    assert not error_elements, 'Unexpected error messages displayed.'
