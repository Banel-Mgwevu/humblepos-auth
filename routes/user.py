# ==================== routes/user.py ====================
"""
User routes module.
Contains user profile management endpoints.
"""

from flask import Blueprint, request, jsonify, current_app
from models import db
from utils.auth import token_required
from utils.validators import validate_name

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """
    Get current authenticated user's information.
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: User data
        401: Unauthorized
    """
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    }), 200


@user_bp.route('/update', methods=['PATCH'])
@token_required
def update_user(current_user):
    """
    Update user's first name and/or last name.
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "first_name": "John",  // optional
            "last_name": "Doe"     // optional
        }
    
    Returns:
        200: Update successful with updated user data
        400: Invalid request data
        401: Unauthorized
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
        
        # Extract fields
        first_name = data.get('first_name', '').strip() if data.get('first_name') else None
        last_name = data.get('last_name', '').strip() if data.get('last_name') else None
        
        # Check if at least one field is provided
        if not first_name and not last_name:
            return jsonify({
                'success': False,
                'message': 'At least one field (first_name or last_name) is required'
            }), 400
        
        # Validate first_name if provided
        if first_name:
            is_valid, error_msg = validate_name(first_name, "First name")
            if not is_valid:
                return jsonify({
                    'success': False,
                    'message': error_msg
                }), 400
            current_user.first_name = first_name
        
        # Validate last_name if provided
        if last_name:
            is_valid, error_msg = validate_name(last_name, "Last name")
            if not is_valid:
                return jsonify({
                    'success': False,
                    'message': error_msg
                }), 400
            current_user.last_name = last_name
        
        # Commit changes to database
        # updated_at will be automatically updated by SQLAlchemy
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User updated successfully',
            'user': current_user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Update error: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'An error occurred while updating user'
        }), 500

