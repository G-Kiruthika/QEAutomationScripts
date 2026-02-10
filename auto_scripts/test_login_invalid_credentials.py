# Test Case: Invalid Credentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_login_invalid_credentials():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://ecommerce.example.com/login')
    driver.find_element(By.ID, 'email').send_keys('invaliduser@example.com')
    driver.find_element(By.ID, 'password').send_keys('WrongPassword')
    driver.find_element(By.ID, 'loginBtn').click()
    time.sleep(2)
    error = driver.find_element(By.ID, 'login-error').text
    assert 'Invalid credentials' in error
    driver.quit()

if __name__ == '__main__':
    test_login_invalid_credentials()
