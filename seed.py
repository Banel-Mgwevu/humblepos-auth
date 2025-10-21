# seed.py
"""
Database seeding script.
Creates initial test users for development and testing.

Usage:
    python seed.py
"""

from app import create_app, init_db
from models import db, User
from utils.auth import hash_password


def seed_users():
    """
    Create test users in the database.
    
    This function creates multiple test users with different roles
    for development and testing purposes.
    """
    app = create_app('development')
    
    with app.app_context():
        # Initialize database if not exists
        init_db(app)
        
        # Test users data
        test_users = [
            {
                'email': 'test@example.com',
                'password': 'password123',
                'first_name': 'Test',
                'last_name': 'User'
            },
            {
                'email': 'john.doe@example.com',
                'password': 'password123',
                'first_name': 'John',
                'last_name': 'Doe'
            },
            {
                'email': 'jane.smith@example.com',
                'password': 'password123',
                'first_name': 'Jane',
                'last_name': 'Smith'
            }
        ]
        
        created_count = 0
        skipped_count = 0
        
        print("\n" + "="*50)
        print("Database Seeding Started")
        print("="*50 + "\n")
        
        for user_data in test_users:
            # Check if user already exists
            existing_user = User.query.filter_by(
                email=user_data['email']
            ).first()
            
            if existing_user:
                print(f"⏭️  Skipped: {user_data['email']} (already exists)")
                skipped_count += 1
                continue
            
            # Create new user
            new_user = User(
                email=user_data['email'],
                password=hash_password(user_data['password']),
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            db.session.add(new_user)
            print(f"✅ Created: {user_data['email']}")
            print(f"   Password: {user_data['password']}")
            created_count += 1
        
        # Commit all changes
        try:
            db.session.commit()
            print("\n" + "="*50)
            print(f"Seeding Complete!")
            print(f"Created: {created_count} users")
            print(f"Skipped: {skipped_count} users")
            print("="*50 + "\n")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error: {str(e)}\n")


def clear_users():
    """
    Clear all users from the database.
    WARNING: This will delete all user data!
    """
    app = create_app('development')
    
    with app.app_context():
        response = input(
            "⚠️  WARNING: This will delete ALL users! "
            "Type 'DELETE' to confirm: "
        )
        
        if response == 'DELETE':
            count = User.query.count()
            User.query.delete()
            db.session.commit()
            print(f"\n✅ Deleted {count} users\n")
        else:
            print("\n❌ Operation cancelled\n")


if __name__ == '__main__':
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--clear':
        clear_users()
    else:
        seed_users()