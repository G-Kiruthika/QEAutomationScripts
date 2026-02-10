# Test Case: Empty Fields
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_login_empty_fields():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://ecommerce.example.com/login')
    driver.find_element(By.ID, 'loginBtn').click()
    time.sleep(1)
    email_error = driver.find_element(By.ID, 'email-error').text
    password_error = driver.find_element(By.ID, 'password-error').text
    assert 'required' in email_error.lower()
    assert 'required' in password_error.lower()
    driver.quit()

if __name__ == '__main__':
    test_login_empty_fields()
