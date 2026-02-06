# TestScripts.py
"""
Automated Selenium test scripts for LoginPage injection validation.
Covers TC-LOGIN-013: SQL and script injection tests.
"""

import unittest
from selenium import webdriver
from LoginPage import LoginPage

class LoginInjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.login_page = LoginPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_sql_injection_login(self):
        """
        TC-LOGIN-013 Steps 2-5: SQL injection payloads in email and password fields.
        """
        self.login_page.navigate_to_login("https://ecommerce.example.com/login")
        sql_email = "admin' OR '1'='1"
        sql_password = "' OR '1'='1"
        result = self.login_page.test_sql_injection(sql_email, sql_password)
        self.assertIn("invalid", result["error_message"].lower())
        self.assertFalse(result["dashboard_visible"], "Dashboard should not be visible after SQL injection attempt.")
        # Check that input is sanitized
        self.assertNotIn("' OR '1'='1", result["email_field_value"])
        self.assertNotIn("' OR '1'='1", result["password_field_value"])

    def test_script_injection_login(self):
        """
        TC-LOGIN-013 Step 6: Script injection payload in email field.
        """
        self.login_page.navigate_to_login("https://ecommerce.example.com/login")
        script_email = "<script>alert('XSS')X\u001a<a href=\"mailto:248X@test.com\">248X@test.com</a>"
        result = self.login_page.test_script_injection(script_email)
        self.assertFalse(result["alert_present"], "Alert should not be present after script injection.")
        self.assertIn("invalid", result["error_message"].lower())
        self.assertFalse(result["script_in_field"], "Script tags should be sanitized and not appear in email field.")

if __name__ == "__main__":
    unittest.main()
