# Test Case: Remember Me Functionality
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_login_remember_me():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://ecommerce.example.com/login')
    driver.find_element(By.ID, 'email').send_keys('validuser@example.com')
    driver.find_element(By.ID, 'password').send_keys('ValidPassword123')
    driver.find_element(By.ID, 'rememberMe').click()
    driver.find_element(By.ID, 'loginBtn').click()
    time.sleep(2)
    cookies = driver.get_cookies()
    driver.quit()
    # Simulate new session
    driver2 = webdriver.Chrome(options=options)
    driver2.get('https://ecommerce.example.com/login')
    for cookie in cookies:
        driver2.add_cookie(cookie)
    driver2.get('https://ecommerce.example.com/dashboard')
    time.sleep(2)
    assert 'dashboard' in driver2.current_url or 'Welcome' in driver2.page_source
    driver2.quit()

if __name__ == '__main__':
    test_login_remember_me()
