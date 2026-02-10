# Test Case: Locked/Disabled Account
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_login_locked_account():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://ecommerce.example.com/login')
    driver.find_element(By.ID, 'email').send_keys('lockeduser@example.com')
    driver.find_element(By.ID, 'password').send_keys('ValidPassword123')
    driver.find_element(By.ID, 'loginBtn').click()
    time.sleep(2)
    error = driver.find_element(By.ID, 'login-error').text
    assert 'locked' in error.lower() or 'disabled' in error.lower()
    driver.quit()

if __name__ == '__main__':
    test_login_locked_account()
