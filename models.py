# ==================== models.py ====================
"""
Database models module.
Contains all SQLAlchemy model definitions.
"""

from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    User model for storing user authentication and profile data.
    
    Attributes:
        id (str): UUID primary key
        email (str): Unique user email address
        password (str): Hashed password
        first_name (str): User's first name
        last_name (str): User's last name
        updated_at (datetime): Timestamp of last update
    """
    
    __tablename__ = 'users'
    
    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )
    password = db.Column(
        db.String(255),
        nullable=False
    )
    first_name = db.Column(
        db.String(100),
        nullable=False
    )
    last_name = db.Column(
        db.String(100),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    def __repr__(self):
        """String representation of User object."""
        return f'<User {self.email}>'
    
    def to_dict(self, include_sensitive=False):
        """
        Convert user object to dictionary.
        
        Args:
            include_sensitive (bool): Whether to include sensitive data
            
        Returns:
            dict: User data as dictionary
        """
        data = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_sensitive:
            data['password'] = self.password
            
        return data

