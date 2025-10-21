# tests/test_validators.py
"""
Validation utility tests.
Tests input validation functions.
"""

import pytest
from utils.validators import validate_email, validate_password, validate_name


class TestEmailValidator:
    """Test cases for email validation."""
    
    def test_valid_emails(self):
        """Test validation of valid email addresses."""
        valid_emails = [
            'test@example.com',
            'user.name@example.com',
            'user+tag@example.co.uk',
            'user123@test-domain.com'
        ]
        for email in valid_emails:
            assert validate_email(email) is True
    
    def test_invalid_emails(self):
        """Test validation of invalid email addresses."""
        invalid_emails = [
            'not-an-email',
            '@example.com',
            'user@',
            'user@domain',
            '',
            None,
            'user @example.com'
        ]
        for email in invalid_emails:
            assert validate_email(email) is False


class TestPasswordValidator:
    """Test cases for password validation."""
    
    def test_valid_passwords(self):
        """Test validation of valid passwords."""
        valid, _ = validate_password('password123')
        assert valid is True
        
        valid, _ = validate_password('a' * 8)
        assert valid is True
    
    def test_short_password(self):
        """Test validation of password too short."""
        valid, error = validate_password('short')
        assert valid is False
        assert 'at least 8 characters' in error
    
    def test_empty_password(self):
        """Test validation of empty password."""
        valid, error = validate_password('')
        assert valid is False
    
    def test_none_password(self):
        """Test validation of None password."""
        valid, error = validate_password(None)
        assert valid is False


class TestNameValidator:
    """Test cases for name validation."""
    
    def test_valid_names(self):
        """Test validation of valid names."""
        valid, _ = validate_name('John')
        assert valid is True
        
        valid, _ = validate_name('Mary-Jane')
        assert valid is True
    
    def test_empty_name(self):
        """Test validation of empty name."""
        valid, error = validate_name('')
        assert valid is False
    
    def test_too_long_name(self):
        """Test validation of name exceeding max length."""
        valid, error = validate_name('a' * 101)
        assert valid is False
        assert 'cannot exceed 100 characters' in error
    
    def test_none_name(self):
        """Test validation of None name."""
        valid, error = validate_name(None)
        assert valid is False