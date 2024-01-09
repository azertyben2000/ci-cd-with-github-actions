import unittest
from app import app
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_item(self):
        # Test adding an item
        response = self.app.post('/add', data=dict(item="Test Item"), follow_redirects=True)
        self.assertEqual(response.status_code, 200, "Response should be 200 OK")

        res = self.app.get('/get')
        self.assertIn(b"Test Item", res.data, "Item should be here")

    def test_delete_item(self):
        
        # Test delete an item
        response = self.app.get('/delete/0', follow_redirects=True)
        self.assertEqual(response.status_code, 200, "Response should be 200 OK")

        response = self.app.get('/get')
        self.assertNotIn(b"Test Item", response.data, "Item should be deleted")

    def test_update_item(self):
        # Test update an item
        self.test_add_item()

        response = self.app.post(
            '/update/0', 
            data={'new_item': 'Updated Item'}, 
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200, "Response should be 200 OK")

        res = self.app.get('/get')
        self.assertIn(b"Updated Item", res.data, "Item should be updated")
        self.assertNotIn(b"Test Item", res.data, "Old Item should not be present")
    
class TestAppE2E(unittest.TestCase):
    def setup_method(self, method):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.driver = webdriver.Firefox(options=opts)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_add_update_delete(self):
        # Launch your flask app first
        self.driver.get("http://127.0.0.1:5000")
        
        # Add item
        self.driver.find_element(By.NAME, "item").click()
        self.driver.find_element(By.NAME, "item").send_keys("item_1")
        self.driver.find_element(By.CSS_SELECTOR, "button").click()
        self.assertIn('item_1', self.driver.page_source)

        # Update
        self.driver.find_element(By.NAME, "new_item").click()
        self.driver.find_element(By.NAME, "new_item").send_keys("item_update")
        self.driver.find_element(By.CSS_SELECTOR, "li button").click()
        self.assertIn('item_update', self.driver.page_source)

        # Delete
        self.driver.find_element(By.LINK_TEXT, "Delete").click()
        self.assertNotIn('item_1', self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
