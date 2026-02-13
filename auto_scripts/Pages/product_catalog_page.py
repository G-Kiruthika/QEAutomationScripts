from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class ProductCatalogPage(BasePage):
    SEARCH_BOX = (By.ID, "searchBox")
    PRODUCT_LIST = (By.CLASS_NAME, "product-list")
    ADD_PRODUCT_BUTTON = (By.ID, "addProductBtn")

    def search_product(self, product_name):
        self.send_keys(self.SEARCH_BOX, product_name)

    def click_add_product(self):
        self.click(self.ADD_PRODUCT_BUTTON)

    def is_product_list_visible(self):
        return self.is_visible(self.PRODUCT_LIST)
