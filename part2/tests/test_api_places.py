import unittest
from run import app
import json

class PlaceAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_create_place(self):
        payload = {
            "name": "Cozy Apartment",
            "description": "A small cozy place",
            "address": "456 Another St",
            "owner_id": "user-123",
            "price": 50.0,
            "latitude": 45.0,
            "longitude": -75.0,
            "amenity_ids": [],
            "review_ids": []
        }
        res = self.client.post('/api/v1/places/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()["name"], "Cozy Apartment")

    def test_get_places(self):
        res = self.client.get('/api/v1/places/')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_create_place_invalid(self):
        payload = {
            "name": "",
            "description": "No name place",
            "address": "No address",
            "owner_id": "user-123",
            "price": -10,
            "latitude": 100,  # invalid latitude
            "longitude": 200,  # invalid longitude
            "amenity_ids": [],
            "review_ids": []
        }
        res = self.client.post('/api/v1/places/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 400)

if __name__ == '__main__':
    unittest.main()
