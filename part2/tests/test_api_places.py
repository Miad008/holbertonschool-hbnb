import unittest
import json
from app import create_app

class PlaceAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()  # Get the Flask app instance
        cls.client = cls.app.test_client()  # Create a test client

    def test_create_place(self):
        # Define a valid payload for creating a place
        payload = {
            "name": "New Place",
            "description": "A new place",
            "location": "Riyadh, Saudi Arabia"
        }
        res = self.client.post('/api/v1/places/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('id', json.loads(res.data))

    def test_create_place_invalid(self):
        # Define an invalid payload (missing 'name' field)
        payload = {
            "description": "A new place without a name"
        }
        res = self.client.post('/api/v1/places/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 400)  # Expecting a bad request due to missing field
        self.assertIn('Missing required place fields', json.loads(res.data))

if __name__ == '__main__':
    unittest.main()
