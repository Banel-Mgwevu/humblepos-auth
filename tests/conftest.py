# tests/conftest.py
"""
Test configuration and fixtures.
Provides reusable test fixtures for all test modules.
"""

import pytest
from app import create_app, init_db
from models import db, User
from utils.auth import hash_password


@pytest.fixture
def app():
    """
    Create and configure a test application instance.
    Uses in-memory SQLite database for testing.
    """
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Create a test client for the application.
    
    Args:
        app: Flask application fixture
        
    Returns:
        FlaskClient: Test client for making requests
    """
    return app.test_client()


@pytest.fixture
def test_user(app):
    """
    Create a test user in the database.
    
    Args:
        app: Flask application fixture
        
    Returns:
        User: Test user object
    """
    with app.app_context():
        user = User(
            email='test@example.com',
            password=hash_password('password123'),
            first_name='Test',
            last_name='User'
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def auth_token(client, test_user):
    """
    Get authentication token for test user.
    
    Args:
        client: Flask test client
        test_user: Test user fixture
        
    Returns:
        str: JWT authentication token
    """
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    data = response.get_json()
    return data['token']





