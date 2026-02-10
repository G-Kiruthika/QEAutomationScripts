# Test Case: Successful Login
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def test_login_success():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://ecommerce.example.com/login')
    driver.find_element(By.ID, 'email').send_keys('validuser@example.com')
    driver.find_element(By.ID, 'password').send_keys('ValidPassword123')
    driver.find_element(By.ID, 'loginBtn').click()
    time.sleep(2)
    assert 'dashboard' in driver.current_url or 'Welcome' in driver.page_source
    driver.quit()

if __name__ == '__main__':
    test_login_success()
