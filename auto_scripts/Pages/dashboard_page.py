from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DashboardPage:
    # Locators from metadata
    WELCOME_BANNER = (By.ID, 'welcomeBanner')
    LOGOUT_BUTTON = (By.ID, 'logoutBtn')
    USER_AVATAR = (By.CSS_SELECTOR, '.user-avatar')
    NOTIFICATIONS_ICON = (By.ID, 'notifIcon')

    def __init__(self, driver):
        self.driver = driver

    # Actions from metadata
    def click_logout(self):
        self.driver.find_element(*self.LOGOUT_BUTTON).click()

    def click_notifications(self):
        self.driver.find_element(*self.NOTIFICATIONS_ICON).click()

    # Validations from metadata
    def is_welcome_banner_displayed(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.WELCOME_BANNER)
        )

    def is_user_avatar_present(self):
        return len(self.driver.find_elements(*self.USER_AVATAR)) > 0
