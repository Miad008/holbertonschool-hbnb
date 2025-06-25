import unittest
from run import app
import json

class AmenityAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_create_amenity(self):
        payload = {
            "name": "Pool"
        }
        res = self.client.post('/api/v1/amenities', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()["name"], "Pool")

    def test_get_amenities(self):
        res = self.client.get('/api/v1/amenities')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_create_amenity_invalid(self):
        payload = {
            "name": ""
        }
        res = self.client.post('/api/v1/amenities', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 400)

if __name__ == '__main__':
    unittest.main()
