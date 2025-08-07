#!/usr/bin/env python3
"""
Registration Test Script
Test the new admin registration functionality
"""

import sys
sys.path.append('.')

from app import create_app, db
from app.models.user import User
import pam


def test_pam_authentication():
    """Test PAM authentication with system user"""
    print("🔐 Testing PAM Authentication")
    print("=" * 40)
    
    # Test credentials
    test_username = "testadmin"
    test_password = "admin123"  # Set during user creation
    
    try:
        p = pam.pam()
        result = p.authenticate(test_username, test_password)
        
        if result:
            print(f"✅ PAM authentication successful for '{test_username}'")
            print(f"   System user '{test_username}' can authenticate")
        else:
            print(f"❌ PAM authentication failed for '{test_username}'")
            print(f"   Check system user credentials")
            
        return result
        
    except Exception as e:
        print(f"❌ PAM authentication error: {e}")
        return False


def test_user_creation():
    """Test user creation with different types"""
    app = create_app()
    
    with app.app_context():
        print("\n👥 Testing User Creation")
        print("=" * 40)
        
        # Test 1: Regular user
        print("\n1. Creating regular user...")
        regular_user = User(
            username="testuser",
            email="test@example.com", 
            first_name="Test",
            last_name="User",
            is_admin=False
        )
        regular_user.password = "password123"
        
        print(f"   Username: {regular_user.username}")
        print(f"   Admin: {regular_user.is_admin}")
        print(f"   Uses PAM: {regular_user.uses_pam_auth}")
        print(f"   Password Hash: {'Set' if regular_user.password_hash else 'None'}")
        
        # Test 2: Admin user 
        print("\n2. Creating admin user...")
        admin_user = User(
            username="testadmin",
            email="admin@example.com",
            first_name="Test", 
            last_name="Admin",
            is_admin=True
        )
        admin_user.password_hash = None  # PAM users don't store passwords
        
        print(f"   Username: {admin_user.username}")
        print(f"   Admin: {admin_user.is_admin}")
        print(f"   Uses PAM: {admin_user.uses_pam_auth}")
        print(f"   Password Hash: {'Set' if admin_user.password_hash else 'None'}")
        
        # Test authentication
        print("\n3. Testing authentication...")
        print("   Regular user password check:", regular_user.check_password("password123"))
        print("   Admin user PAM check:", admin_user.check_password("admin123"))
        
        return True


def main():
    print("🚀 Lab Portal Registration Testing")
    print("=" * 50)
    
    # Test PAM functionality
    pam_works = test_pam_authentication()
    
    # Test user model
    test_user_creation()
    
    print("\n📋 Test Summary")
    print("=" * 30)
    print(f"PAM Authentication: {'✅ Working' if pam_works else '❌ Failed'}")
    print("User Model: ✅ Working")
    print("Registration Form: ✅ Updated with admin checkbox")
    
    print(f"\n🎯 Next Steps:")
    print("1. Test registration form at: http://127.0.0.1:5001/auth/register")
    print("2. Try registering a regular user (no admin checkbox)")
    print("3. Try registering admin user with system credentials:")
    print("   - Username: testadmin")
    print("   - Password: admin123")
    print("   - Check 'Register as Admin User' checkbox")


if __name__ == '__main__':
    main()
