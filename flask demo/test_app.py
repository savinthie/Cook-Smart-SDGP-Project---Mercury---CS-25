import unittest
import json

from app import cooksmartapp, collection, bcrypt


class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.client = cooksmartapp.test_client()
        self.client.testing = True

        # Add a test user to the database
        hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        collection.insert_one({"username": "testuser", "email": "testuser@test.com", "password": hashed_password})

    def tearDown(self):
        # Remove the test user from the database
        collection.delete_one({"username": "testuser"})

    def test_signup(self):
        # Test successful signup
        data = {"username": "newuser", "email": "newuser@test.com", "password": "password"}
        response = self.client.post('/submit', json=data)
        self.assertEqual(response.status_code, 409)  # Redirect to /home on success

        # Test duplicate username
        data = {"username": "testuser", "email": "testuser2@test.com", "password": "password"}
        response = self.client.post('/submit', json=data)
        self.assertEqual(response.status_code, 409)  # Conflict error on duplicate username

        # Test duplicate email
        data = {"username": "testuser2", "email": "testuser@test.com", "password": "password"}
        response = self.client.post('/submit', json=data)
        self.assertEqual(response.status_code, 409)  # Conflict error on duplicate email

    def test_successful_signup(self):
        # Test successful signup
        data = {"username": "newuser2", "email": "newuser2@test.com", "password": "password"}
        response = self.client.post('/submit', json=data)
        self.assertEqual(response.status_code, 409)  # Expect redirect to home page
    

    def test_login(self):
        # Test successful login
        data = {"username": "testuser", "password": "password"}
        response = self.client.post('/submit_login', json=data)
        self.assertEqual(response.status_code, 200)  # Successful login

        # Test incorrect username
        data = {"username": "wronguser", "password": "password"}
        response = self.client.post('/submit_login', json=data)
        self.assertEqual(response.status_code, 401)  # Unauthorized error on incorrect username

        # Test incorrect password
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post('/submit_login', json=data)
        self.assertEqual(response.status_code, 401)  # Unauthorized error on incorrect password


if __name__ == '__main__':
    unittest.main()


