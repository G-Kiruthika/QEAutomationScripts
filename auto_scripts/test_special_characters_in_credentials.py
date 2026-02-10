from selenium import webdriver
from selenium.webdriver.common.by import By
import time

LOGIN_URL = 'https://example-ecommerce.com/login'
valid_special_username = 'user+test@example.com'
valid_special_password = 'P@ssw0rd!'
invalid_special_username = 'user<>@example.com'
invalid_special_password = 'P@ssw0rd<>!'

with webdriver.Chrome() as driver:
    driver.get(LOGIN_URL)
    # Valid special characters
    driver.find_element(By.ID, 'username').send_keys(valid_special_username)
    driver.find_element(By.ID, 'password').send_keys(valid_special_password)
    driver.find_element(By.ID, 'login-button').click()
    time.sleep(1)
    assert driver.current_url != LOGIN_URL, 'Valid special characters rejected.'
    driver.get(LOGIN_URL)
    # Invalid special characters
    driver.find_element(By.ID, 'username').send_keys(invalid_special_username)
    driver.find_element(By.ID, 'password').send_keys(invalid_special_password)
    driver.find_element(By.ID, 'login-button').click()
    time.sleep(1)
    error = driver.find_element(By.CLASS_NAME, 'error-message')
    assert error.is_displayed(), 'No error for invalid special characters.'
    assert driver.current_url == LOGIN_URL, 'User should remain on login page.'
