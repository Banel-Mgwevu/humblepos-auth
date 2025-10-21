# app.py
"""
Main application module.
Creates and configures the Flask application using environment variables.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import get_config
from models import db
from routes.auth import auth_bp
from routes.user import user_bp


def create_app(config_name=None):
    """
    Application factory function.
    Creates and configures a Flask application instance.
    
    Args:
        config_name (str): Configuration name (development/production/testing)
                          If None, uses FLASK_ENV from environment
        
    Returns:
        Flask: Configured Flask application
    """
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration from environment variables
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Initialize configuration-specific settings
    config_class.init_app(app)
    
    # Initialize extensions
    initialize_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register general routes
    register_general_routes(app)
    
    # Log configuration info
    app.logger.info(f"Application started in {app.config['FLASK_ENV']} mode")
    app.logger.info(f"Database: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1]}")
    
    return app


def initialize_extensions(app):
    """
    Initialize Flask extensions.
    
    Args:
        app (Flask): Flask application instance
    """
    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Initialize CORS
    CORS(app, resources={
        r"/*": {
            "origins": app.config['CORS_ORIGINS']
        }
    })
    
    app.logger.info(f"CORS enabled for origins: {app.config['CORS_ORIGINS']}")


def register_blueprints(app):
    """
    Register application blueprints.
    
    Args:
        app (Flask): Flask application instance
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    
    app.logger.info("Blueprints registered: auth, user")


def register_error_handlers(app):
    """
    Register application error handlers.
    
    Args:
        app (Flask): Flask application instance
    """
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({
            'success': False,
            'message': 'Resource not found',
            'error': 'Not Found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors."""
        return jsonify({
            'success': False,
            'message': 'Method not allowed',
            'error': 'Method Not Allowed'
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        db.session.rollback()
        app.logger.error(f'Internal error: {str(error)}')
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': 'Internal Server Error'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle uncaught exceptions."""
        db.session.rollback()
        app.logger.error(f'Unhandled exception: {str(error)}', exc_info=True)
        
        # Don't expose internal errors in production
        if app.config['DEBUG']:
            return jsonify({
                'success': False,
                'message': str(error),
                'error': 'Exception'
            }), 500
        else:
            return jsonify({
                'success': False,
                'message': 'An unexpected error occurred',
                'error': 'Internal Server Error'
            }), 500


def register_general_routes(app):
    """
    Register general application routes.
    
    Args:
        app (Flask): Flask application instance
    """
    
    @app.route('/', methods=['GET'])
    def index():
        """Root endpoint with API information."""
        return jsonify({
            'success': True,
            'name': app.config['APP_NAME'],
            'version': app.config['APP_VERSION'],
            'environment': app.config['FLASK_ENV'],
            'endpoints': {
                'health': '/health',
                'login': '/auth/login',
                'user_info': '/user/me',
                'user_update': '/user/update'
            }
        }), 200
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint for monitoring."""
        try:
            # Test database connection
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            db_status = 'connected'
        except Exception as e:
            app.logger.error(f'Database health check failed: {str(e)}')
            db_status = 'disconnected'
        
        is_healthy = db_status == 'connected'
        status_code = 200 if is_healthy else 503
        
        return jsonify({
            'success': is_healthy,
            'message': 'API is running' if is_healthy else 'API is unhealthy',
            'status': 'healthy' if is_healthy else 'unhealthy',
            'database': db_status,
            'environment': app.config['FLASK_ENV']
        }), status_code


def init_db(app):
    """
    Initialize database tables.
    
    Args:
        app (Flask): Flask application instance
    """
    with app.app_context():
        # Import models to register them with SQLAlchemy
        from models import User
        
        # Create all tables
        db.create_all()
        app.logger.info('Database tables created successfully')


def setup_logging(app):
    """
    Setup application logging.
    
    Args:
        app (Flask): Flask application instance
    """
    if not app.debug and not app.testing:
        import logging
        from logging.handlers import RotatingFileHandler
        import os
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(app.config['LOG_FILE'])
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Setup file handler
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'],
            maxBytes=app.config['LOG_MAX_BYTES'],
            backupCount=app.config['LOG_BACKUP_COUNT']
        )
        
        # Set log format
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        
        # Set log level
        log_level = getattr(logging, app.config['LOG_LEVEL'].upper(), logging.INFO)
        file_handler.setLevel(log_level)
        
        # Add handler to app logger
        app.logger.addHandler(file_handler)
        app.logger.setLevel(log_level)
        
        app.logger.info(f'Logging configured: {app.config["LOG_FILE"]}')


if __name__ == '__main__':
    # Create application
    app = create_app()
    
    # Setup logging
    setup_logging(app)
    
    # Initialize database
    init_db(app)
    
    # Run application
    # For production, use Gunicorn or uWSGI instead
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )