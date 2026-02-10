# Test Case: Input Validation (Invalid Email Format)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_login_input_validation():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://ecommerce.example.com/login')
    driver.find_element(By.ID, 'email').send_keys('invalid-email-format')
    driver.find_element(By.ID, 'password').send_keys('SomePassword123')
    driver.find_element(By.ID, 'loginBtn').click()
    time.sleep(1)
    email_error = driver.find_element(By.ID, 'email-error').text
    assert 'invalid email' in email_error.lower()
    driver.quit()

if __name__ == '__main__':
    test_login_input_validation()
