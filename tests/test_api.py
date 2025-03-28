import unittest
import os
import tempfile
from app import create_app, db
from app.models import User, File

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
        # Create test user
        self.test_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
    def test_user_registration(self):
        response = self.client.post('/auth/register', 
                                  json=self.test_user_data)
        self.assertEqual(response.status_code, 201)
        
    def test_user_login(self):
        # Register user first
        self.client.post('/auth/register', json=self.test_user_data)
        
        # Try logging in
        response = self.client.post('/auth/login', json={
            'email': self.test_user_data['email'],
            'password': self.test_user_data['password']
        })
        self.assertEqual(response.status_code, 200)
        
    def test_file_upload(self):
        # Login first
        self.client.post('/auth/register', json=self.test_user_data)
        self.client.post('/auth/login', json={
            'email': self.test_user_data['email'],
            'password': self.test_user_data['password']
        })
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.txt') as tf:
            tf.write(b'Test content')
            tf.seek(0)
            
            response = self.client.post('/upload',
                                      data={'file': (tf, 'test.txt')},
                                      content_type='multipart/form-data')
            
        self.assertEqual(response.status_code, 201)
        
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()