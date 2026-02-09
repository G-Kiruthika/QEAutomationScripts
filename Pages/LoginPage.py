# LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LoginPage:
    """
    Page Object Model for the Login Page.
    Provides methods to interact with login elements and validate login behaviors.
    """

    def __init__(self, driver, timeout=10):
        """
        Initializes LoginPage with WebDriver instance and timeout.
        :param driver: Selenium WebDriver instance
        :param timeout: Default wait timeout in seconds
        """
        self.driver = driver
        self.timeout = timeout

    def enter_username(self, username):
        """
        Enters the username into the username field.
        :param username: Username string
        :raises ValueError: If username is not a string or too short
        """
        if not isinstance(username, str):
            raise ValueError("Username must be a string.")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        username_field = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#username"))
        )
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password):
        """
        Enters the password into the password field.
        :param password: Password string
        :raises ValueError: If password is not a string
        """
        if not isinstance(password, str):
            raise ValueError("Password must be a string.")
        password_field = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#password"))
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        """
        Clicks the login button.
        """
        login_button = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button#login"))
        )
        login_button.click()

    def is_login_successful(self):
        """
        Checks if login was successful by verifying the presence of the dashboard element.
        :return: True if dashboard is present, False otherwise
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.dashboard"))
            )
            return True
        except TimeoutException:
            return False

    def is_captcha_present(self):
        """
        Checks if CAPTCHA widget is present after failed login attempts.
        :return: True if CAPTCHA is present, False otherwise
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.captcha"))
            )
            return True
        except TimeoutException:
            return False

    def is_lock_message_present(self):
        """
        Checks if account lock message is displayed after repeated failed login attempts.
        :return: True if lock message is present, False otherwise
        """
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.lock-message"))
            )
            return True
        except TimeoutException:
            return False

    def login(self, username, password):
        """
        Performs the complete login action.
        :param username: Username string
        :param password: Password string
        :return: True if login is successful, False otherwise
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self.is_login_successful()

    def attempt_login_multiple_times(self, username, password, attempts=3):
        """
        Attempts to login multiple times with given credentials.
        Used to simulate repeated failed login attempts for lock/CAPTCHA scenarios.
        :param username: Username string
        :param password: Password string
        :param attempts: Number of attempts
        :return: Tuple (is_locked, is_captcha)
        """
        for i in range(attempts):
            try:
                self.enter_username(username)
                self.enter_password(password)
                self.click_login()
            except Exception as e:
                # Log exception, continue
                print(f"Login attempt {i+1} failed: {e}")
        is_locked = self.is_lock_message_present()
        is_captcha = self.is_captcha_present()
        return (is_locked, is_captcha)

    def get_lock_message_text(self):
        """
        Returns the lock message text if present.
        :return: Lock message text, or None
        """
        try:
            lock_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.lock-message"))
            )
            return lock_elem.text
        except TimeoutException:
            return None

    def get_captcha_text(self):
        """
        Returns the CAPTCHA widget text if present.
        :return: CAPTCHA text, or None
        """
        try:
            captcha_elem = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.captcha"))
            )
            return captcha_elem.text
        except TimeoutException:
            return None

# End of LoginPage.py
