# ==================== utils/auth.py ====================
"""
Authentication utilities module.
Contains JWT token handling and password hashing functions.
"""

import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models import User


def hash_password(password):
    """
    Hash a password using Werkzeug's security functions.
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    method = current_app.config.get('PASSWORD_HASH_METHOD', 'pbkdf2:sha256')
    return generate_password_hash(password, method=method)


def verify_password(password_hash, password):
    """
    Verify a password against its hash.
    
    Args:
        password_hash (str): Hashed password
        password (str): Plain text password to verify
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return check_password_hash(password_hash, password)


def generate_token(user_id):
    """
    Generate a JWT token for authenticated users.
    
    Args:
        user_id (str): User's unique identifier
        
    Returns:
        str: Encoded JWT token
    """
    expiration = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES')
    algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')
    secret_key = current_app.config.get('JWT_SECRET_KEY')
    
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + expiration,
        'iat': datetime.utcnow()
    }
    
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_token(token):
    """
    Decode and verify a JWT token.
    
    Args:
        token (str): JWT token to decode
        
    Returns:
        dict: Token payload if valid, None otherwise
    """
    try:
        secret_key = current_app.config.get('JWT_SECRET_KEY')
        algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')
        
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """
    Decorator to protect routes requiring authentication.
    Validates JWT token and injects current_user into route function.
    
    Usage:
        @app.route('/protected')
        @token_required
        def protected_route(current_user):
            return jsonify({'user': current_user.to_dict()})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Extract token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Authentication token is missing'
            }), 401
        
        # Decode token
        payload = decode_token(token)
        
        if not payload:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token'
            }), 401
        
        # Get user from database
        current_user = User.query.get(payload.get('user_id'))
        
        if not current_user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 401
        
        # Pass current_user to the decorated function
        return f(current_user, *args, **kwargs)
    
    return decorated

