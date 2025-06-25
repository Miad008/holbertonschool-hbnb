import unittest
import json
from app import create_app

class PlaceAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test client."""
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_create_place(self):
        """Test creating a valid place."""
        payload = {
            "name": "Beach House",
            "address": "123 Beach Ave",
            "owner_id": "owner_id_123",
            "price": 200
        }

        res = self.client.post('/api/v1/places/', data=json.dumps(payload), content_type='application/json')

        # Assert that the status code is 201 (Created)
        self.assertEqual(res.status_code, 201)

        # Assert that the place is created successfully
        data = json.loads(res.data)
        self.assertEqual(data['name'], "Beach House")

    def test_create_place_invalid(self):
        """Test creating a place with missing fields."""
        payload = {
            # Missing 'address', 'owner_id', and 'price' fields
        }

        res = self.client.post('/api/v1/places/', data=json.dumps(payload), content_type='application/json')

        # Assert that the status code is 400 (Bad Request)
        self.assertEqual(res.status_code, 400)

        # Check if the error message is correct
        data = json.loads(res.data)
        self.assertEqual(data['error'], "Missing required place fields")
