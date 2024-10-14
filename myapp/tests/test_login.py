from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginTests(LiveServerTestCase):

    def setUp(self):
        super().setUp()
        self.driver = webdriver.Chrome()  # Ensure this matches your ChromeDriver setup
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()
        super().tearDown()

    def test_customer_login(self):
        self.driver.get('http://127.0.0.1:8000/login/')  # Use live_server_url for dynamic URL
        email_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')

        email_input.send_keys('delnatheres2003@gmail.com')
        password_input.send_keys('Delna@123')
        password_input.send_keys(Keys.RETURN)

        WebDriverWait(self.driver, 10).until(
            EC.url_contains("customer-dashboard")
        )
        self.assertIn("Customer Dashboard", self.driver.title) 

    def test_admin_login(self):
        self.driver.get(self.live_server_url + '/login/')
        email_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')

        email_input.send_keys('admin@gmail.com')
        password_input.send_keys('admin123')
        password_input.send_keys(Keys.RETURN)

        WebDriverWait(self.driver, 10).until(
            EC.url_contains("admin-dashboard")
        )
        self.assertIn("Admin Dashboard", self.driver.title)

    def test_employee_login(self):
        self.driver.get(self.live_server_url + '/login/')
        email_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')

        email_input.send_keys('sharonjo@gmail.com')
        password_input.send_keys('Sharon@123')
        password_input.send_keys(Keys.RETURN)

        WebDriverWait(self.driver, 10).until(
            EC.url_contains("employee-dashboard")
        )
        self.assertIn("Employee Dashboard", self.driver.title)
