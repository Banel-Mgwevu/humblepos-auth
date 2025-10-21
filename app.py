
# ==================== app.py ====================
"""
Main application module.
Creates and configures the Flask application.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from models import db
from routes.auth import auth_bp
from routes.user import user_bp


def create_app(config_name=None):
    """
    Application factory function.
    Creates and configures a Flask application instance.
    
    Args:
        config_name (str): Configuration name (development/production/testing)
        
    Returns:
        Flask: Configured Flask application
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={
        r"/*": {
            "origins": app.config['CORS_ORIGINS']
        }
    })
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register general routes
    register_general_routes(app)
    
    return app


def register_error_handlers(app):
    """Register application error handlers."""
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({
            'success': False,
            'message': 'Resource not found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors."""
        return jsonify({
            'success': False,
            'message': 'Method not allowed'
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


def register_general_routes(app):
    """Register general application routes."""
    
    @app.route('/', methods=['GET'])
    def index():
        """Root endpoint with API information."""
        return jsonify({
            'success': True,
            'message': 'Authentication API',
            'version': '1.0',
            'endpoints': {
                'health': '/health',
                'login': '/auth/login',
                'user_info': '/user/me',
                'user_update': '/user/update'
            }
        }), 200
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'success': True,
            'message': 'API is running',
            'status': 'healthy'
        }), 200


def init_db(app):
    """
    Initialize database tables.
    
    Args:
        app (Flask): Flask application instance
    """
    with app.app_context():
        db.create_all()
        app.logger.info('Database tables created successfully')


if __name__ == '__main__':
    # Create application
    app = create_app()
    
    # Initialize database
    init_db(app)
    
    # Run application
    # For production, use Gunicorn or uWSGI instead
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )