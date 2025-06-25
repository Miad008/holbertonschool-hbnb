import unittest
import json
from app import create_app

class UserAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()  # Get the Flask app instance
        cls.client = cls.app.test_client()  # Create a test client

    def test_create_user(self):
        # Define a valid payload for creating a user
        payload = {
            "email": "testuser@example.com",
            "password": "testpassword"
        }
        res = self.client.post('/api/v1/users/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('id', json.loads(res.data))

    def test_create_user_invalid(self):
        # Define an invalid payload (missing 'password' field)
        payload = {
            "email": "testuser@example.com"
        }
        res = self.client.post('/api/v1/users/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 400)  # Expecting a bad request due to missing field
        self.assertIn('Missing required user fields', json.loads(res.data))

if __name__ == '__main__':
    unittest.main()
