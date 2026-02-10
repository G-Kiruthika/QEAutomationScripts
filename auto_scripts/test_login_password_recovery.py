# Test Case: Password Recovery
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_login_password_recovery():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://ecommerce.example.com/login')
    driver.find_element(By.LINK_TEXT, 'Forgot Password?').click()
    time.sleep(1)
    driver.find_element(By.ID, 'recovery-email').send_keys('validuser@example.com')
    driver.find_element(By.ID, 'recoverBtn').click()
    time.sleep(2)
    msg = driver.find_element(By.ID, 'recovery-message').text
    assert 'email has been sent' in msg.lower()
    driver.quit()

if __name__ == '__main__':
    test_login_password_recovery()
