import unittest
import json
from app import create_app

class UserAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test client."""
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_create_user(self):
        """Test creating a valid user."""
        payload = {
            "username": "john_doe",
            "email": "john.doe@example.com",
            "password": "password123"
        }

        res = self.client.post('/api/v1/users/', data=json.dumps(payload), content_type='application/json')

        # Assert that the status code is 201 (Created)
        self.assertEqual(res.status_code, 201)

        # Assert that the user is created successfully
        data = json.loads(res.data)
        self.assertEqual(data['username'], "john_doe")
        self.assertEqual(data['email'], "john.doe@example.com")

    def test_create_user_invalid(self):
        """Test creating a user with missing fields."""
        payload = {
            # Missing 'email' and 'password' fields
            "username": "jane_doe"
        }

        res = self.client.post('/api/v1/users/', data=json.dumps(payload), content_type='application/json')

        # Assert that the status code is 400 (Bad Request)
        self.assertEqual(res.status_code, 400)

        # Check if the error message is correct
        data = json.loads(res.data)
        self.assertEqual(data['error'], "Missing required user fields")

    def test_get_user(self):
        """Test retrieving a user's information."""
        # First, create a user to fetch it
        create_payload = {
            "username": "alice_smith",
            "email": "alice.smith@example.com",
            "password": "securePassword"
        }
        create_res = self.client.post('/api/v1/users/', data=json.dumps(create_payload), content_type='application/json')
        created_user = json.loads(create_res.data)

        # Retrieve the user using the ID or username (assuming an endpoint for getting a user)
        res = self.client.get(f'/api/v1/users/{created_user["id"]}')
        
        # Assert that the status code is 200 (OK)
        self.assertEqual(res.status_code, 200)

        # Assert that the user's information is correct
        data = json.loads(res.data)
        self.assertEqual(data['username'], "alice_smith")
        self.assertEqual(data['email'], "alice.smith@example.com")

    def test_update_user(self):
        """Test updating a user's information."""
        # First, create a user to update it
        create_payload = {
            "username": "bob_jones",
            "email": "bob.jones@example.com",
            "password": "oldPassword"
        }
        create_res = self.client.post('/api/v1/users/', data=json.dumps(create_payload), content_type='application/json')
        created_user = json.loads(create_res.data)

        # Update the user's email
        update_payload = {
            "email": "bob.jones_updated@example.com"
        }

        res = self.client.put(f'/api/v1/users/{created_user["id"]}', data=json.dumps(update_payload), content_type='application/json')

        # Assert that the status code is 200 (OK)
        self.assertEqual(res.status_code, 200)

        # Assert that the user's email was updated
        data = json.loads(res.data)
        self.assertEqual(data['email'], "bob.jones_updated@example.com")

    def test_delete_user(self):
        """Test deleting a user."""
        # First, create a user to delete it
        create_payload = {
            "username": "charlie_brown",
            "email": "charlie.brown@example.com",
            "password": "password456"
        }
        create_res = self.client.post('/api/v1/users/', data=json.dumps(create_payload), content_type='application/json')
        created_user = json.loads(create_res.data)

        # Now, delete the user
        res = self.client.delete(f'/api/v1/users/{created_user["id"]}')

        # Assert that the status code is 204 (No Content, successfully deleted)
        self.assertEqual(res.status_code, 204)

        # Try to retrieve the deleted user to check if it was deleted
        res = self.client.get(f'/api/v1/users/{created_user["id"]}')
        
        # Assert that the user was not found (404)
        self.assertEqual(res.status_code, 404)
