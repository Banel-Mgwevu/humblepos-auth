# debug_login.py
"""
Debug login issues by checking database and user setup.
"""

import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
DB_NAME = os.getenv('DB_NAME', 'ysw_data')


def check_users():
    """Check what users exist in the database."""
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print("\n" + "="*70)
        print("CHECKING DATABASE USERS")
        print("="*70 + "\n")
        
        with connection.cursor() as cursor:
            # Check table structure
            print("1. Checking table structure...")
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            
            print("\n   Columns in 'users' table:")
            for col in columns:
                print(f"   - {col['Field']:<20} {col['Type']:<20} {col['Null']}")
            
            # Count users
            print("\n2. Checking users...")
            cursor.execute("SELECT COUNT(*) as count FROM users")
            result = cursor.fetchone()
            user_count = result['count']
            
            print(f"   Total users in database: {user_count}")
            
            if user_count == 0:
                print("\n   ❌ NO USERS FOUND!")
                print("   Run this command to create test users:")
                print("   python seed.py")
                return False
            
            # Show all users (without passwords)
            print("\n3. Users in database:")
            cursor.execute("SELECT id, email, first_name, last_name, updated_at FROM users")
            users = cursor.fetchall()
            
            for user in users:
                print(f"\n   Email: {user['email']}")
                print(f"   Name:  {user['first_name']} {user['last_name']}")
                print(f"   ID:    {user['id']}")
            
            # Check if password column has data
            print("\n4. Checking passwords...")
            cursor.execute("SELECT email, LENGTH(password) as pwd_len FROM users")
            pwd_check = cursor.fetchall()
            
            all_have_passwords = True
            for user in pwd_check:
                if user['pwd_len'] == 0 or user['pwd_len'] is None:
                    print(f"   ❌ {user['email']} - NO PASSWORD SET")
                    all_have_passwords = False
                else:
                    print(f"   ✓ {user['email']} - Password set ({user['pwd_len']} chars)")
            
            if not all_have_passwords:
                print("\n   ❌ Some users don't have passwords!")
                print("   Run this command to fix:")
                print("   python seed.py --clear")
                print("   python seed.py")
                return False
            
            print("\n" + "="*70)
            print("✓ DATABASE LOOKS GOOD")
            print("="*70)
            print("\nYou should be able to login with:")
            print("  Email:    test@example.com")
            print("  Password: password123")
            print("\nTest with:")
            print('  curl -X POST http://localhost:5000/auth/login \\')
            print('    -H "Content-Type: application/json" \\')
            print('    -d \'{"email":"test@example.com","password":"password123"}\'')
            
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        return False
    finally:
        connection.close()


if __name__ == '__main__':
    check_users()