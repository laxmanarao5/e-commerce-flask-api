import unittest
import json
from app import create_app  # Import the Flask app

app = create_app()

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # This method runs before each test case
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_products(self):
        # Simulate a GET request to the home route
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Welcome to the Flask app!')

    # def test_addition_success(self):
    #     # Simulate a POST request to the add route with valid data
    #     response = self.client.post('/add', data=json.dumps({'x': 5, 'y': 7}), content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     self.assertEqual(data['result'], 12)

    # def test_addition_missing_params(self):
    #     # Simulate a POST request to the add route with missing parameters
    #     response = self.client.post('/add', data=json.dumps({'x': 5}), content_type='application/json')
    #     self.assertEqual(response.status_code, 400)
    #     data = json.loads(response.data)
    #     self.assertEqual(data['error'], 'Missing parameters')

    def tearDown(self):
        # This method runs after each test case
        pass

if __name__ == '__main__':
    unittest.main()
