#!/usr/bin/env python
"""
PAM Test CLI
Simple test for PAM authentication functionality
"""

import sys
import os
sys.path.append('/home/tonny/projects/lab_portal')

from app import create_app, db
from app.models.user import User


def main():
    """Test PAM authentication"""
    app = create_app()
    
    with app.app_context():
        print("=== PAM Authentication Test ===\n")
        
        # Check current users
        users = User.query.all()
        print(f"Current users in database: {len(users)}")
        
        for user in users:
            auth_type = "PAM (Admin)" if user.is_admin else "Database"
            print(f"  • {user.username} - {auth_type}")
        
        print("\n=== PAM Requirements ===")
        print("✅ Admin users MUST use PAM authentication")
        print("✅ Regular users use database authentication") 
        print("✅ No toggle - determined by admin role")
        
        # Check if we have any admin users
        admin_users = User.query.filter_by(is_admin=True).all()
        
        if admin_users:
            print(f"\n=== Admin Users Found ({len(admin_users)}) ===")
            for admin in admin_users:
                print(f"  • {admin.username} - Uses PAM: {admin.uses_pam_auth}")
                print(f"    Password hash: {'None (PAM)' if admin.password_hash is None else 'Set (ERROR)'}")
        else:
            print("\n❌ No admin users found")
            print("   Need to create an admin user for PAM testing")
        
        print("\n=== Next Steps ===")
        print("1. Create a system user account (adduser)")
        print("2. Create corresponding admin user in Lab Portal") 
        print("3. Test login with system credentials")
        
        return True


if __name__ == '__main__':
    main()
