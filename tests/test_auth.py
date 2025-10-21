# tests/test_auth.py
"""
Authentication endpoint tests.
Tests login functionality and token generation.
"""

import pytest
from models import User
from utils.auth import hash_password


class TestLogin:
    """Test cases for login endpoint."""
    
    def test_login_success(self, client, test_user):
        """Test successful login with valid credentials."""
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'token' in data
        assert 'user' in data
        assert data['user']['email'] == 'test@example.com'
    
    def test_login_invalid_email(self, client, test_user):
        """Test login with non-existent email."""
        response = client.post('/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
        assert 'Invalid email or password' in data['message']
    
    def test_login_invalid_password(self, client, test_user):
        """Test login with incorrect password."""
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
    
    def test_login_missing_email(self, client):
        """Test login without email field."""
        response = client.post('/auth/login', json={
            'password': 'password123'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_login_missing_password(self, client):
        """Test login without password field."""
        response = client.post('/auth/login', json={
            'email': 'test@example.com'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_login_empty_body(self, client):
        """Test login with empty request body."""
        response = client.post('/auth/login', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_login_invalid_email_format(self, client):
        """Test login with invalid email format."""
        response = client.post('/auth/login', json={
            'email': 'not-an-email',
            'password': 'password123'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_login_case_insensitive_email(self, client, test_user):
        """Test that email is case-insensitive."""
        response = client.post('/auth/login', json={
            'email': 'TEST@EXAMPLE.COM',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
