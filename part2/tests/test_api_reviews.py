import unittest
from run import app
import json

class ReviewAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_create_review(self):
        payload = {
            "text": "Great place!",
            "user_id": "user-123",
            "place_id": "place-456"
        }
        res = self.client.post('/api/v1/reviews', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()["text"], "Great place!")

    def test_get_reviews(self):
        res = self.client.get('/api/v1/reviews')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_create_review_invalid(self):
        payload = {
            "text": "",
            "user_id": "nonexistent-user",
            "place_id": "nonexistent-place"
        }
        res = self.client.post('/api/v1/reviews', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 400)

if __name__ == '__main__':
    unittest.main()
