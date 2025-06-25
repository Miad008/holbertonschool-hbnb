import unittest
from app import app
import json

class UserAPITestCase(unittest.TestCase):
    def setUp(self):
        """تهيئة بيئة الاختبار"""
        self.client = app.test_client()
        self.client.testing = True

    def test_create_user_miad(self):
        """إنشاء المستخدم Miad Alzahrani"""
        payload = {
            "first_name": "Miad",
            "last_name": "Alzahrani",
            "email": "miad@example.com"
        }
        res = self.client.post('/api/v1/users', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()["first_name"], "Miad")

    def test_create_user_batoul(self):
        """إنشاء المستخدم Batoul Alsaeed"""
        payload = {
            "first_name": "Batoul",
            "last_name": "Alsaeed",
            "email": "batoul@example.com"
        }
        res = self.client.post('/api/v1/users', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()["first_name"], "Batoul")

    def test_create_user_rawa(self):
        """إنشاء المستخدم Rawa Albaraiki"""
        payload = {
            "first_name": "Rawa",
            "last_name": "Albaraiki",
            "email": "rawa@example.com"
        }
        res = self.client.post('/api/v1/users', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()["first_name"], "Rawa")

    def test_get_users(self):
        """جلب جميع المستخدمين"""
        res = self.client.get('/api/v1/users')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

if __name__ == '__main__':
    unittest.main()
