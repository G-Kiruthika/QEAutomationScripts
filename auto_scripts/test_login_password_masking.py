# Test Case: Password Masking
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def test_login_password_masking():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://ecommerce.example.com/login')
    password_field = driver.find_element(By.ID, 'password')
    field_type = password_field.get_attribute('type')
    assert field_type == 'password'
    driver.quit()

if __name__ == '__main__':
    test_login_password_masking()
