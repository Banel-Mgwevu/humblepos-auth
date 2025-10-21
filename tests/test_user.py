# tests/test_user.py
"""
User management endpoint tests.
Tests user profile retrieval and updates.
"""

import pytest


class TestGetCurrentUser:
    """Test cases for getting current user info."""
    
    def test_get_user_success(self, client, auth_token):
        """Test getting user info with valid token."""
        response = client.get(
            '/user/me',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'user' in data
        assert data['user']['email'] == 'test@example.com'
    
    def test_get_user_no_token(self, client):
        """Test getting user info without token."""
        response = client.get('/user/me')
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
    
    def test_get_user_invalid_token(self, client):
        """Test getting user info with invalid token."""
        response = client.get(
            '/user/me',
            headers={'Authorization': 'Bearer invalid-token'}
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False


class TestUpdateUser:
    """Test cases for updating user profile."""
    
    def test_update_first_name(self, client, auth_token):
        """Test updating only first name."""
        response = client.patch(
            '/user/update',
            headers={'Authorization': f'Bearer {auth_token}'},
            json={'first_name': 'John'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['user']['first_name'] == 'John'
        assert data['user']['last_name'] == 'User'  # Unchanged
    
    def test_update_last_name(self, client, auth_token):
        """Test updating only last name."""
        response = client.patch(
            '/user/update',
            headers={'Authorization': f'Bearer {auth_token}'},
            json={'last_name': 'Doe'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['user']['first_name'] == 'Test'  # Unchanged
        assert data['user']['last_name'] == 'Doe'
    
    def test_update_both_names(self, client, auth_token):
        """Test updating both first and last name."""
        response = client.patch(
            '/user/update',
            headers={'Authorization': f'Bearer {auth_token}'},
            json={
                'first_name': 'John',
                'last_name': 'Doe'
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['user']['first_name'] == 'John'
        assert data['user']['last_name'] == 'Doe'
    
    def test_update_no_fields(self, client, auth_token):
        """Test update without any fields."""
        response = client.patch(
            '/user/update',
            headers={'Authorization': f'Bearer {auth_token}'},
            json={}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_update_empty_first_name(self, client, auth_token):
        """Test update with empty first name."""
        response = client.patch(
            '/user/update',
            headers={'Authorization': f'Bearer {auth_token}'},
            json={'first_name': ''}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_update_too_long_name(self, client, auth_token):
        """Test update with name exceeding max length."""
        long_name = 'a' * 101  # Exceeds 100 character limit
        response = client.patch(
            '/user/update',
            headers={'Authorization': f'Bearer {auth_token}'},
            json={'first_name': long_name}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_update_no_token(self, client):
        """Test update without authentication token."""
        response = client.patch(
            '/user/update',
            json={'first_name': 'John'}
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
    
    def test_update_invalid_token(self, client):
        """Test update with invalid token."""
        response = client.patch(
            '/user/update',
            headers={'Authorization': 'Bearer invalid-token'},
            json={'first_name': 'John'}
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert data['success'] is False
    
    def test_update_whitespace_trimming(self, client, auth_token):
        """Test that whitespace is trimmed from names."""
        response = client.patch(
            '/user/update',
            headers={'Authorization': f'Bearer {auth_token}'},
            json={
                'first_name': '  John  ',
                'last_name': '  Doe  '
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['first_name'] == 'John'
        assert data['user']['last_name'] == 'Doe'

