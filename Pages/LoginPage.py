import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    URL = "https://example-ecommerce.com/login"
    LOCATORS = {
        "emailField": (By.ID, "login-email"),
        "passwordField": (By.ID, "login-password"),
        "rememberMeCheckbox": (By.ID, "remember-me"),
        "loginSubmit": (By.ID, "login-submit"),
        "forgotPasswordLink": (By.CSS_SELECTOR, "a.forgot-password-link"),
        "errorMessage": (By.CSS_SELECTOR, "div.alert-danger"),
        "validationError": (By.CSS_SELECTOR, ".invalid-feedback"),
        "emptyFieldPrompt": (By.XPATH, "//*[contains(text(),'Mandatory fields are required')]") ,
        "dashboardHeader": (By.CSS_SELECTOR, "h1.dashboard-title"),
        "userProfileIcon": (By.CSS_SELECTOR, ".user-profile-name")
    }

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def navigate(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.LOCATORS["emailField"]))
        self.wait.until(EC.visibility_of_element_located(self.LOCATORS["passwordField"]))
        self.wait.until(EC.visibility_of_element_located(self.LOCATORS["loginSubmit"]))

    def enter_email(self, email):
        email_elem = self.wait.until(EC.visibility_of_element_located(self.LOCATORS["emailField"]))
        email_elem.clear()
        email_elem.send_keys(email)

    def enter_password(self, password):
        pwd_elem = self.wait.until(EC.visibility_of_element_located(self.LOCATORS["passwordField"]))
        pwd_elem.clear()
        pwd_elem.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOCATORS["loginSubmit"]))
        login_btn.click()

    def validate_accessibility(self):
        # Screen reader: ARIA attributes
        email_elem = self.wait.until(EC.visibility_of_element_located(self.LOCATORS["emailField"]))
        password_elem = self.wait.until(EC.visibility_of_element_located(self.LOCATORS["passwordField"]))
        login_btn = self.wait.until(EC.visibility_of_element_located(self.LOCATORS["loginSubmit"]))
        accessibility_results = {}
        accessibility_results["email_aria_label"] = email_elem.get_attribute("aria-label") is not None
        accessibility_results["password_aria_label"] = password_elem.get_attribute("aria-label") is not None
        accessibility_results["login_btn_aria_label"] = login_btn.get_attribute("aria-label") is not None
        # Keyboard navigation: Tab order
        self.driver.find_element(By.TAG_NAME, "body").click()
        tab_order = []
        for _ in range(3):
            self.driver.find_element(By.TAG_NAME, "body").send_keys("\t")
            active = self.driver.switch_to.active_element
            tab_order.append(active.get_attribute("id"))
        accessibility_results["tab_order"] = tab_order
        # Color contrast: CSS values
        color_contrast = {}
        for field in [email_elem, password_elem, login_btn]:
            fg = field.value_of_css_property("color")
            bg = field.value_of_css_property("background-color")
            color_contrast[field.get_attribute("id")] = {"fg": fg, "bg": bg}
        accessibility_results["color_contrast"] = color_contrast
        return accessibility_results

    def is_password_masked(self):
        pwd_elem = self.wait.until(EC.visibility_of_element_located(self.LOCATORS["passwordField"]))
        input_type = pwd_elem.get_attribute("type")
        return input_type == "password"

    def get_error_message(self):
        try:
            error_elem = self.wait.until(EC.visibility_of_element_located(self.LOCATORS["errorMessage"]))
            return error_elem.text
        except TimeoutException:
            return None

    def get_validation_error(self):
        try:
            validation_elem = self.wait.until(EC.visibility_of_element_located(self.LOCATORS["validationError"]))
            return validation_elem.text
        except TimeoutException:
            return None

    def is_empty_field_prompt_displayed(self):
        try:
            prompt_elem = self.wait.until(EC.visibility_of_element_located(self.LOCATORS["emptyFieldPrompt"]))
            return True
        except TimeoutException:
            return False

    def is_logged_in(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.LOCATORS["dashboardHeader"]))
            self.wait.until(EC.visibility_of_element_located(self.LOCATORS["userProfileIcon"]))
            return True
        except TimeoutException:
            return False
