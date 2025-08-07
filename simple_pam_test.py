#!/usr/bin/env python3
"""
Simple PAM Test
Direct PAM authentication test
"""

import pam
import getpass

def test_pam_simple():
    """Simple PAM test"""
    username = "testadmin"
    password = getpass.getpass(f"Enter password for {username}: ")
    
    try:
        p = pam.pam()
        result = p.authenticate(username, password)
        
        if result:
            print(f"✅ PAM authentication successful for '{username}'")
        else:
            print(f"❌ PAM authentication failed for '{username}'")
            
        return result
        
    except Exception as e:
        print(f"❌ PAM error: {e}")
        return False

if __name__ == '__main__':
    test_pam_simple()
