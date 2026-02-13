from selenium.webdriver.common.by import By

class LoginPage:
    LOGIN_URL = "https://example.com/login"
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "loginBtn")
    VALIDATION_ERROR = (By.CSS_SELECTOR, ".validation-error")
    ACCOUNT_LOCKOUT_MESSAGE = (By.CSS_SELECTOR, ".account-lockout")
    EMAIL_NOTIFICATION = (By.CSS_SELECTOR, ".email-notification")

    def navigate_to_login_page(self, driver):
        driver.get(self.LOGIN_URL)

    def enter_username(self, driver, username):
        driver.find_element(*self.USERNAME_INPUT).send_keys(username)

    def enter_password(self, driver, password):
        driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def click_login_button(self, driver):
        driver.find_element(*self.LOGIN_BUTTON).click()

    def verify_validation_error(self, driver):
        return driver.find_element(*self.VALIDATION_ERROR).is_displayed()

    def verify_login_prevented(self, driver):
        return not driver.find_element(*self.LOGIN_BUTTON).is_enabled()

    def verify_account_lockout_message(self, driver):
        return driver.find_element(*self.ACCOUNT_LOCKOUT_MESSAGE).is_displayed()

    def verify_email_notification_sent(self, driver):
        return driver.find_element(*self.EMAIL_NOTIFICATION).is_displayed()
