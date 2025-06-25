import unittest
import json
from app import create_app

class ReviewAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()  # Get the Flask app instance
        cls.client = cls.app.test_client()  # Create a test client

    def test_create_review(self):
        # Define a valid payload for creating a review
        payload = {
            "place_id": "1",
            "user_id": "1",
            "review": "Great place!"
        }
        res = self.client.post('/api/v1/reviews/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('id', json.loads(res.data))

    def test_create_review_invalid(self):
        # Define an invalid payload (missing 'review' field)
        payload = {
            "place_id": "1",
            "user_id": "1"
        }
        res = self.client.post('/api/v1/reviews/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 400)  # Expecting a bad request due to missing field
        self.assertIn('Missing required review fields', json.loads(res.data))

if __name__ == '__main__':
    unittest.main()
