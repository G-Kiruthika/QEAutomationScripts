from selenium import webdriver
from selenium.webdriver.common.by import By
import time

LOGIN_URL = 'https://example-ecommerce.com/login'
USERNAME = 'valid_user@example.com'
INVALID_PASSWORD = 'WrongPassword!'
MAX_ATTEMPTS = 3

with webdriver.Chrome() as driver:
    driver.get(LOGIN_URL)
    for attempt in range(MAX_ATTEMPTS):
        driver.find_element(By.ID, 'username').clear()
        driver.find_element(By.ID, 'password').clear()
        driver.find_element(By.ID, 'username').send_keys(USERNAME)
        driver.find_element(By.ID, 'password').send_keys(INVALID_PASSWORD)
        driver.find_element(By.ID, 'login-button').click()
        time.sleep(1)
    # After max attempts, lockout or CAPTCHA should appear
    lockout = driver.find_elements(By.ID, 'lockout-message')
    captcha = driver.find_elements(By.ID, 'captcha')
    assert lockout or captcha, 'Lockout or CAPTCHA not enforced after multiple failed attempts.'
    message = driver.find_element(By.CLASS_NAME, 'error-message')
    assert message.is_displayed(), 'Appropriate message not displayed.'
    # Optional: simulate waiting for lockout reset if policy allows
