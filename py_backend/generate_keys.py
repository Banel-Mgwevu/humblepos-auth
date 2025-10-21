# # generate_keys.py
# """
# Generate secure keys and automatically update .env file.
# This script generates SECRET_KEY and JWT_SECRET_KEY and updates your .env file.

# Usage:
#     python generate_keys.py
# """

# import secrets
# import os
# import sys
# from pathlib import Path


# def generate_secure_key():
#     """Generate a secure random key."""
#     return secrets.token_hex(32)


# def update_env_file():
#     """Update .env file with newly generated keys."""
#     env_path = Path('.env')
    
#     # Check if .env exists
#     if not env_path.exists():
#         print("❌ Error: .env file not found!")
#         print("💡 Tip: Copy .env.example to .env first")
#         return False
    
#     # Read current .env content
#     with open(env_path, 'r') as f:
#         lines = f.readlines()
    
#     # Generate new keys
#     new_secret_key = generate_secure_key()
#     new_jwt_key = generate_secure_key()
    
#     print("\n" + "="*60)
#     print("🔑 Generating Secure Keys".center(60))
#     print("="*60 + "\n")
    
#     # Track if keys were found and updated
#     secret_key_updated = False
#     jwt_key_updated = False
    
#     # Update lines
#     new_lines = []
#     for line in lines:
#         if line.startswith('SECRET_KEY='):
#             old_value = line.split('=', 1)[1].strip()
#             if old_value and not old_value.startswith('your-'):
#                 response = input(f"⚠️  SECRET_KEY already set. Replace? (y/N): ")
#                 if response.lower() != 'y':
#                     new_lines.append(line)
#                     print("   Keeping existing SECRET_KEY")
#                     secret_key_updated = True
#                     continue
            
#             new_lines.append(f'SECRET_KEY={new_secret_key}\n')
#             print(f"✅ SECRET_KEY updated")
#             secret_key_updated = True
            
#         elif line.startswith('JWT_SECRET_KEY='):
#             old_value = line.split('=', 1)[1].strip()
#             if old_value and not old_value.startswith('your-'):
#                 response = input(f"⚠️  JWT_SECRET_KEY already set. Replace? (y/N): ")
#                 if response.lower() != 'y':
#                     new_lines.append(line)
#                     print("   Keeping existing JWT_SECRET_KEY")
#                     jwt_key_updated = True
#                     continue
            
#             new_lines.append(f'JWT_SECRET_KEY={new_jwt_key}\n')
#             print(f"✅ JWT_SECRET_KEY updated")
#             jwt_key_updated = True
            
#         else:
#             new_lines.append(line)
    
#     # Write updated content back
#     with open(env_path, 'w') as f:
#         f.writelines(new_lines)
    
#     print("\n" + "="*60)
    
#     if secret_key_updated and jwt_key_updated:
#         print("✅ Keys successfully generated and saved to .env")
#     else:
#         print("⚠️  Warning: Some keys were not found in .env file")
#         print("   Make sure your .env has these lines:")
#         print("   SECRET_KEY=your-super-secret-key-change-this")
#         print("   JWT_SECRET_KEY=your-jwt-secret-key-change-this")
    
#     print("="*60 + "\n")
    
#     return True


# def display_keys():
#     """Display generated keys without updating file."""
#     print("\n" + "="*60)
#     print("🔑 Generated Secure Keys".center(60))
#     print("="*60 + "\n")
    
#     secret_key = generate_secure_key()
#     jwt_key = generate_secure_key()
    
#     print("Copy these to your .env file:\n")
#     print(f"SECRET_KEY={secret_key}")
#     print(f"JWT_SECRET_KEY={jwt_key}")
#     print("\n" + "="*60 + "\n")


# def main():
#     """Main function."""
#     print("\n🔐 Flask Auth API - Key Generator")
    
#     # Check for command line arguments
#     if len(sys.argv) > 1:
#         if sys.argv[1] == '--display-only':
#             display_keys()
#             return
#         elif sys.argv[1] == '--help':
#             print("\nUsage:")
#             print("  python generate_keys.py              # Update .env file")
#             print("  python generate_keys.py --display-only  # Just show keys")
#             print("  python generate_keys.py --help       # Show this help")
#             return
    
#     # Check if .env exists
#     if not Path('.env').exists():
#         print("\n❌ Error: .env file not found!")
#         print("\nPlease create .env file first:")
#         print("  cp .env.example .env")
#         print("\nOr create a basic .env with these lines:")
#         print("  SECRET_KEY=your-super-secret-key-change-this")
#         print("  JWT_SECRET_KEY=your-jwt-secret-key-change-this")
#         sys.exit(1)
    
#     # Update .env file
#     success = update_env_file()
    
#     if success:
#         print("✅ You can now run the application:")
#         print("   python app.py")
#     else:
#         sys.exit(1)


# if __name__ == '__main__':
#     main()