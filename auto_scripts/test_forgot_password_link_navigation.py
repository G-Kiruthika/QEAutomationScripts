from selenium import webdriver
from selenium.webdriver.common.by import By
import time

LOGIN_URL = 'https://example-ecommerce.com/login'
RECOVERY_URL = 'https://example-ecommerce.com/password-recovery'

with webdriver.Chrome() as driver:
    driver.get(LOGIN_URL)
    driver.find_element(By.LINK_TEXT, 'Forgot Password?').click()
    time.sleep(2)
    try:
        assert driver.current_url == RECOVERY_URL, 'Did not navigate to password recovery page.'
    except AssertionError:
        error = driver.find_element(By.CLASS_NAME, 'error-message')
        assert error.is_displayed(), 'User-friendly error not displayed if recovery page fails.'
