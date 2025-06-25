import unittest
import json
from app import create_app

class ReviewAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test client."""
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_create_review(self):
        """Test creating a valid review."""
        payload = {
            "user_id": "user_123",
            "place_id": "place_123",
            "text": "Great place, highly recommended!"
        }

        res = self.client.post('/api/v1/reviews/', data=json.dumps(payload), content_type='application/json')

        # Assert that the status code is 201 (Created)
        self.assertEqual(res.status_code, 201)

        # Assert that the review is created successfully
        data = json.loads(res.data)
        self.assertEqual(data['text'], "Great place, highly recommended!")

    def test_create_review_invalid(self):
        """Test creating a review with missing fields."""
        payload = {
            # Missing 'user_id', 'place_id', and 'text' fields
        }

        res = self.client.post('/api/v1/reviews/', data=json.dumps(payload), content_type='application/json')

        # Assert that the status code is 400 (Bad Request)
        self.assertEqual(res.status_code, 400)

        # Check if the error message is correct
        data = json.loads(res.data)
        self.assertEqual(data['error'], "Missing required review fields")

