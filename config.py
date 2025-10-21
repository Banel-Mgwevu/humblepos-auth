# config.py
"""
Application configuration module.
Loads all configuration from environment variables (.env file).
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Application configuration loaded from environment variables.
    All settings are read from .env file or environment.
    """
    
    # ==================== Flask Settings ====================
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in .env file")
    
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
    TESTING = os.getenv('TESTING', 'False').lower() in ('true', '1', 'yes')
    
    # ==================== Database Settings ====================
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL must be set in .env file")
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False').lower() in ('true', '1', 'yes')
    
    # Database connection pool settings (optional)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.getenv('DB_POOL_SIZE', 10)),
        'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 3600)),
        'pool_pre_ping': True,
        'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', 20))
    }
    
    # ==================== JWT Settings ====================
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv('JWT_EXPIRATION_HOURS', 24))
    )
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    
    # ==================== CORS Settings ====================
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS]
    
    # ==================== Security Settings ====================
    PASSWORD_MIN_LENGTH = int(os.getenv('PASSWORD_MIN_LENGTH', 8))
    PASSWORD_HASH_METHOD = os.getenv('PASSWORD_HASH_METHOD', 'pbkdf2:sha256')
    PASSWORD_SALT_LENGTH = int(os.getenv('PASSWORD_SALT_LENGTH', 16))
    
    # ==================== Application Settings ====================
    APP_NAME = os.getenv('APP_NAME', 'Flask Auth API')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    
    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # ==================== Logging Settings ====================
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10485760))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 10))
    
    # ==================== Environment ====================
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    @staticmethod
    def init_app(app):
        """
        Initialize application with additional configuration.
        Called after app is created.
        
        Args:
            app: Flask application instance
        """
        pass


class DevelopmentConfig(Config):
    """
    Development environment configuration.
    Inherits from Config and can override specific settings.
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True
    
    @classmethod
    def init_app(cls, app):
        """Initialize development-specific settings."""
        Config.init_app(app)
        app.logger.info('Development mode enabled')


class ProductionConfig(Config):
    """
    Production environment configuration.
    Enforces stricter security requirements.
    """
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    @classmethod
    def init_app(cls, app):
        """Initialize production-specific settings."""
        Config.init_app(app)
        
        # Validate required environment variables
        required_vars = [
            'SECRET_KEY',
            'DATABASE_URL',
            'JWT_SECRET_KEY'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables in production: "
                f"{', '.join(missing_vars)}"
            )
        
        # Validate CORS is not set to wildcard in production
        if '*' in cls.CORS_ORIGINS:
            app.logger.warning(
                "WARNING: CORS_ORIGINS is set to '*' in production. "
                "This is not recommended for security reasons."
            )
        
        app.logger.info('Production mode enabled')


class TestingConfig(Config):
    """
    Testing environment configuration.
    Uses in-memory database for fast testing.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    @classmethod
    def init_app(cls, app):
        """Initialize testing-specific settings."""
        Config.init_app(app)
        app.logger.info('Testing mode enabled')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """
    Get configuration class based on environment.
    
    Args:
        config_name (str, optional): Configuration name
        
    Returns:
        Config: Configuration class
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    return config.get(config_name, config['default'])