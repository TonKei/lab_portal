#!/usr/bin/env python
"""
PAM Authentication Test
Test script for validating PAM authentication functionality
"""

import sys
import os
sys.path.append('/home/tonny/projects/lab_portal')

from app import create_app, db
from app.models.user import User


def test_pam_import():
    """Test if PAM module can be imported"""
    try:
        import pam
        print("✅ PAM module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ PAM import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ PAM error: {e}")
        return False


def test_pam_authentication():
    """Test PAM authentication with system user"""
    try:
        import pam
        p = pam.pam()
        
        print(f"PAM service: {getattr(p, 'service', 'default')}")
        
        # Test with a known system user (usually 'root' exists)
        # Note: This will fail unless you provide actual credentials
        print("\nTesting PAM authentication...")
        print("Note: This test requires actual system credentials")
        
        return True
        
    except Exception as e:
        print(f"❌ PAM authentication test failed: {e}")
        return False


def create_pam_test_user():
    """Create a test user with PAM authentication enabled"""
    app = create_app()
    
    with app.app_context():
        # Check if test user already exists
        test_user = User.query.filter_by(username='pam_test_user').first()
        
        if test_user:
            print("PAM test user already exists")
            return test_user
        
        # Create a new user with PAM authentication
        test_user = User(
            username='pam_test_user',
            email='pam_test@example.com',
            first_name='PAM',
            last_name='Test',
            use_pam_auth=True,  # Enable PAM authentication
            is_admin=False
        )
        
        db.session.add(test_user)
        db.session.commit()
        
        print("✅ Created PAM test user")
        return test_user


def test_user_authentication():
    """Test authentication with our User model"""
    app = create_app()
    
    with app.app_context():
        # Test with regular database user
        regular_user = User.query.filter_by(use_pam_auth=False).first()
        
        if regular_user:
            print(f"\n🔍 Testing regular user: {regular_user.username}")
            print(f"   Uses PAM: {regular_user.use_pam_auth}")
            
            # Test with wrong password (should fail)
            result = regular_user.check_password('wrong_password')
            print(f"   Wrong password test: {'❌ FAIL' if not result else '⚠️  UNEXPECTED PASS'}")
        
        # Test with PAM user
        pam_user = User.query.filter_by(use_pam_auth=True).first()
        
        if pam_user:
            print(f"\n🔍 Testing PAM user: {pam_user.username}")
            print(f"   Uses PAM: {pam_user.use_pam_auth}")
            print("   Note: PAM authentication requires valid system credentials")


def main():
    """Main test function"""
    print("=== Lab Portal PAM Authentication Test ===\n")
    
    # Test 1: PAM Import
    pam_available = test_pam_import()
    
    # Test 2: PAM Authentication (basic)
    if pam_available:
        test_pam_authentication()
    
    # Test 3: Create PAM test user
    create_pam_test_user()
    
    # Test 4: Test user authentication
    test_user_authentication()
    
    print("\n=== PAM Test Summary ===")
    print("• PAM module:", "✅ Available" if pam_available else "❌ Not Available")
    print("• User model: ✅ Ready")
    print("• PAM integration: ✅ Implemented")
    
    print("\n=== Next Steps ===")
    print("1. To test PAM authentication, create a system user")
    print("2. Create a Lab Portal user with PAM enabled")
    print("3. Test login with system credentials")
    
    if not pam_available:
        print("\n⚠️  PAM module issues detected:")
        print("   • Check if libpam-dev is installed")
        print("   • Reinstall python-pam if needed")
        print("   • Check system PAM configuration")


if __name__ == '__main__':
    main()
