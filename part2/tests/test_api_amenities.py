import unittest
import json
from app import create_app

class AmenityAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()  # Get the Flask app instance
        cls.client = cls.app.test_client()  # Create a test client

    def test_create_amenity(self):
        # Define a valid payload for creating an amenity
        payload = {
            "name": "New Amenity",
            "description": "A new amenity"
        }
        res = self.client.post('/api/v1/amenities/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('id', json.loads(res.data))

    def test_create_amenity_invalid(self):
        # Define an invalid payload (missing 'name' field)
        payload = {
            "description": "A new amenity without a name"
        }
        res = self.client.post('/api/v1/amenities/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 400)  # Expecting a bad request due to missing field
        self.assertIn('Missing required amenity fields', json.loads(res.data))

if __name__ == '__main__':
    unittest.main()
