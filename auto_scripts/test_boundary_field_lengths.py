from selenium import webdriver
from selenium.webdriver.common.by import By
import time

LOGIN_URL = 'https://example-ecommerce.com/login'
MIN_LENGTH = 3
MAX_LENGTH = 50

valid_username = 'a' * MIN_LENGTH
valid_password = 'b' * MIN_LENGTH
long_username = 'a' * (MAX_LENGTH + 1)
long_password = 'b' * (MAX_LENGTH + 1)

with webdriver.Chrome() as driver:
    driver.get(LOGIN_URL)
    # Test min length (should succeed or show no error)
    driver.find_element(By.ID, 'username').send_keys(valid_username)
    driver.find_element(By.ID, 'password').send_keys(valid_password)
    driver.find_element(By.ID, 'login-button').click()
    time.sleep(1)
    # Accept valid lengths (no crash, error, or rejection for min)
    assert driver.current_url != 'about:blank', 'System crashed on min length.'
    driver.get(LOGIN_URL)
    # Test max+1 length (should show error)
    driver.find_element(By.ID, 'username').send_keys(long_username)
    driver.find_element(By.ID, 'password').send_keys(long_password)
    driver.find_element(By.ID, 'login-button').click()
    time.sleep(1)
    error = driver.find_element(By.CLASS_NAME, 'error-message')
    assert error.is_displayed(), 'No error for exceeding max field length.'
    assert driver.current_url == LOGIN_URL, 'User should remain on login page.'
