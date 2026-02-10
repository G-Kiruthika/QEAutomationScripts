from selenium import webdriver
from selenium.webdriver.common.by import By
import time

USERNAME = 'valid_user@example.com'
PASSWORD = 'ValidPassword123'
LOGIN_URL = 'https://example-ecommerce.com/login'
DASHBOARD_URL = 'https://example-ecommerce.com/dashboard'

with webdriver.Chrome() as driver:
    driver.get(LOGIN_URL)
    driver.find_element(By.ID, 'username').send_keys(USERNAME)
    driver.find_element(By.ID, 'password').send_keys(PASSWORD)
    driver.find_element(By.ID, 'remember-me').click()
    driver.find_element(By.ID, 'login-button').click()
    time.sleep(2)
    assert driver.current_url == DASHBOARD_URL, 'Did not redirect to dashboard.'
    # Simulate browser restart
    cookies = driver.get_cookies()
    driver.quit()
    driver2 = webdriver.Chrome()
    driver2.get(DASHBOARD_URL)
    for cookie in cookies:
        driver2.add_cookie(cookie)
    driver2.refresh()
    time.sleep(1)
    assert driver2.current_url == DASHBOARD_URL, 'Session did not persist.'
    # Logout
    driver2.find_element(By.ID, 'logout-button').click()
    time.sleep(1)
    assert not driver2.get_cookie('session_token'), 'Session token should be cleared after logout.'
    driver2.quit()
