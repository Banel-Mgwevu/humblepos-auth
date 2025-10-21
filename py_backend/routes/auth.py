# ==================== routes/auth.py ====================
"""
Authentication routes module.
Contains login and authentication-related endpoints.
"""

from flask import Blueprint, request, jsonify, current_app
from models import db, User
from utils.auth import verify_password, generate_token
from utils.validators import validate_email

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token.
    
    Request Body:
        {
            "email": "user@example.com",
            "password": "userpassword"
        }
    
    Returns:
        200: Login successful with token and user data
        400: Invalid request data
        401: Invalid credentials
        500: Server error
    """
    try:
        # Parse request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Extract and normalize email
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validate required fields
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Validate email format
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        # Use same error message for both cases to prevent user enumeration
        if not user or not verify_password(user.password, password):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Generate JWT token
        token = generate_token(user.id)
        
        # Return success response
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Login error: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'An error occurred during login'
        }), 500

