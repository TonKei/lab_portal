#!/usr/bin/env python3
"""
User Management CLI
Direct database user management for Lab Portal
"""

import sys
import os
sys.path.append('.')

from app import create_app, db
from app.models.user import User


def list_users():
    """List all users in the database"""
    users = User.query.all()
    print(f"\n📋 Total Users: {len(users)}")
    print("=" * 50)
    
    for user in users:
        auth_method = "PAM (System)" if user.is_admin else "Database"
        status = "Admin" if user.is_admin else "Regular"
        print(f"• {user.username:15} | {status:7} | {auth_method}")
        if user.email:
            print(f"  Email: {user.email}")
        print()
    return users


def delete_user(username):
    """Delete a user by username"""
    user = User.query.filter_by(username=username).first()
    if user:
        print(f"🗑️  Deleting user: {user.username}")
        db.session.delete(user)
        db.session.commit()
        print("✅ User deleted successfully")
        return True
    else:
        print(f"❌ User '{username}' not found")
        return False


def main():
    app = create_app()
    
    with app.app_context():
        print("🚀 Lab Portal User Management")
        print("=" * 40)
        
        # List current users
        users = list_users()
        
        # Delete tonny user if exists
        tonny_user = User.query.filter_by(username='tonny').first()
        if tonny_user:
            print(f"\n🎯 Found 'tonny' user - deleting...")
            delete_user('tonny')
            
            print("\n📋 Updated user list:")
            list_users()
        else:
            print("\n✅ No 'tonny' user found in database")
        
        return True


if __name__ == '__main__':
    main()
