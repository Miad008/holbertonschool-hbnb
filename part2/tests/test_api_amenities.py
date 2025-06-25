import unittest
import json
from app import create_app

class AmenityAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test client."""
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_create_amenity(self):
        """Test creating a valid amenity."""
        payload = {
            "name": "Swimming Pool"  # Valid payload for creating amenity
        }

        res = self.client.post('/api/v1/amenities/', data=json.dumps(payload), content_type='application/json')

        # Assert that the status code is 201 (Created)
        self.assertEqual(res.status_code, 201)

        # Assert that the amenity is created successfully
        data = json.loads(res.data)
        self.assertEqual(data['name'], "Swimming Pool")

    def test_create_amenity_invalid(self):
        """Test creating an amenity with missing fields."""
        payload = {
            # Missing 'name' field, this should fail
        }

        res = self.client.post('/api/v1/amenities/', data=json.dumps(payload), content_type='application/json')

        # Assert that the status code is 400 (Bad Request)
        self.assertEqual(res.status_code, 400)

        # Check if the error message is correct
        data = json.loads(res.data)
        self.assertEqual(data['error'], "Missing required amenity fields")

