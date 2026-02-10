from selenium import webdriver
from selenium.webdriver.common.by import By
import time

USERNAME = 'invalid_user@example.com'
PASSWORD = 'WrongPassword!'
LOGIN_URL = 'https://example-ecommerce.com/login'

with webdriver.Chrome() as driver:
    driver.get(LOGIN_URL)
    driver.find_element(By.ID, 'username').send_keys(USERNAME)
    driver.find_element(By.ID, 'password').send_keys(PASSWORD)
    driver.find_element(By.ID, 'login-button').click()
    time.sleep(2)
    error = driver.find_element(By.CLASS_NAME, 'error-message')
    assert error.is_displayed(), 'Error message not displayed.'
    assert not driver.get_cookie('session_token'), 'Session token should not be generated.'
    assert driver.current_url == LOGIN_URL, 'User should remain on login page.'
