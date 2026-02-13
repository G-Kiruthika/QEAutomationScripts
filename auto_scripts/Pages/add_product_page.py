from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class AddProductPage(BasePage):
    PRODUCT_NAME_INPUT = (By.ID, "productName")
    PRODUCT_PRICE_INPUT = (By.ID, "productPrice")
    SAVE_BUTTON = (By.ID, "saveBtn")

    def enter_product_name(self, name):
        self.send_keys(self.PRODUCT_NAME_INPUT, name)

    def enter_product_price(self, price):
        self.send_keys(self.PRODUCT_PRICE_INPUT, price)

    def click_save(self):
        self.click(self.SAVE_BUTTON)

    def is_save_button_visible(self):
        return self.is_visible(self.SAVE_BUTTON)
