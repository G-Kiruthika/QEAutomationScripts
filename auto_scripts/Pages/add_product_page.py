from selenium.webdriver.common.by import By
from auto_scripts.Pages.base_page import BasePage

class AddProductPage(BasePage):
    PRODUCT_NAME_INPUT = (By.ID, "productName")
    PRODUCT_PRICE_INPUT = (By.ID, "productPrice")
    SAVE_BUTTON = (By.ID, "saveBtn")
    # Added from metadata
    ADD_PRODUCT_NAV_LOCATOR = (By.ID, "placeholder_add_product_nav_locator")
    ADD_PRODUCT_FORM_LOCATOR = (By.ID, "placeholder_add_product_form_locator")
    ADD_PRODUCT_FORM_DISPLAY_LOCATOR = (By.ID, "placeholder_add_product_form_display_locator")
    PRODUCT_CREATED_LOCATOR = (By.ID, "placeholder_product_created_locator")

    def enter_product_name(self, name):
        self.send_keys(self.PRODUCT_NAME_INPUT, name)

    def enter_product_price(self, price):
        self.send_keys(self.PRODUCT_PRICE_INPUT, price)

    def click_save(self):
        self.click(self.SAVE_BUTTON)

    def is_save_button_visible(self):
        return self.is_visible(self.SAVE_BUTTON)

    # Added from metadata
    def navigate_to_add_product(self):
        """Navigate to the add product page."""
        self.click(self.ADD_PRODUCT_NAV_LOCATOR)

    def enter_product_details_and_submit(self, product_name, price, inventory, etc):
        """Enter all required product details and submit."""
        self.send_keys(self.ADD_PRODUCT_FORM_LOCATOR, product_name)
        self.send_keys(self.ADD_PRODUCT_FORM_LOCATOR, price)
        self.send_keys(self.ADD_PRODUCT_FORM_LOCATOR, inventory)
        self.send_keys(self.ADD_PRODUCT_FORM_LOCATOR, etc)
        self.click(self.SAVE_BUTTON)

    def assert_add_product_form_displayed(self):
        """Verify add product form is displayed."""
        return self.is_visible(self.ADD_PRODUCT_FORM_DISPLAY_LOCATOR)

    def assert_product_created_successfully(self):
        """Verify product is created and appears in the product list."""
        return self.is_visible(self.PRODUCT_CREATED_LOCATOR)
