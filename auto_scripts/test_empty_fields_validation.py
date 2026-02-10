from selenium import webdriver
from selenium.webdriver.common.by import By
import time

LOGIN_URL = 'https://example-ecommerce.com/login'

with webdriver.Chrome() as driver:
    driver.get(LOGIN_URL)
    # Leave both fields empty
    driver.find_element(By.ID, 'login-button').click()
    time.sleep(1)
    username_error = driver.find_element(By.ID, 'username-error')
    password_error = driver.find_element(By.ID, 'password-error')
    assert username_error.is_displayed(), 'Username required error not displayed.'
    assert password_error.is_displayed(), 'Password required error not displayed.'
    assert not driver.get_cookie('session_token'), 'Session token should not be generated.'
    assert driver.current_url == LOGIN_URL, 'User should remain on login page.'
