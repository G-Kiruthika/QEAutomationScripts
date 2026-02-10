# Test Case: Unregistered User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_login_unregistered_user():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://ecommerce.example.com/login')
    driver.find_element(By.ID, 'email').send_keys('notregistered@example.com')
    driver.find_element(By.ID, 'password').send_keys('SomePassword123')
    driver.find_element(By.ID, 'loginBtn').click()
    time.sleep(2)
    error = driver.find_element(By.ID, 'login-error').text
    assert 'not registered' in error.lower()
    driver.quit()

if __name__ == '__main__':
    test_login_unregistered_user()
