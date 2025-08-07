"""
Authentication Tests
Tests for authentication routes and functionality
"""

import pytest
from flask import url_for
from app.models.user import User
from app import db


@pytest.mark.auth
class TestAuthRoutes:
    """Test authentication routes."""
    
    def test_login_page(self, client):
        """Test login page displays correctly."""
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'Login' in response.data
        assert b'Username' in response.data
        assert b'Password' in response.data
    
    def test_register_page(self, client):
        """Test register page displays correctly."""
        response = client.get('/auth/register')
        assert response.status_code == 200
        assert b'Register' in response.data
        assert b'Username' in response.data
        assert b'Email' in response.data
    
    def test_successful_login(self, client, regular_user):
        """Test successful user login."""
        response = client.post('/auth/login', data={
            'username': regular_user.username,
            'password': 'testpassword123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should redirect to dashboard after successful login
        assert b'Dashboard' in response.data or b'Welcome' in response.data
    
    def test_failed_login_wrong_password(self, client, regular_user):
        """Test login with wrong password."""
        response = client.post('/auth/login', data={
            'username': regular_user.username,
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 200
        assert b'Invalid username or password' in response.data
    
    def test_failed_login_nonexistent_user(self, client):
        """Test login with nonexistent user."""
        response = client.post('/auth/login', data={
            'username': 'nonexistent',
            'password': 'anypassword'
        })
        
        assert response.status_code == 200
        assert b'Invalid username or password' in response.data
    
    def test_logout(self, logged_in_user):
        """Test user logout."""
        response = logged_in_user.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to login page after logout
        assert b'Login' in response.data
    
    def test_user_registration(self, client, app_context):
        """Test user registration."""
        # Clear any existing users first
        User.query.delete()
        db.session.commit()
        
        # Create a dummy admin user first so new user won't become admin
        dummy_admin = User(
            username='dummyadmin',
            email='dummy@example.com',
            first_name='Dummy',
            last_name='Admin',
            password='dummy123',
            is_admin=True
        )
        db.session.add(dummy_admin)
        db.session.commit()
        
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpassword123',
            'password2': 'newpassword123'  # Fixed field name
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Check for success message
        assert b'Registration successful!' in response.data
        
        # Check user was created in database
        user = User.query.filter_by(username='newuser').first()
        assert user is not None
        assert user.email == 'newuser@example.com'
        assert user.first_name == 'New'
        assert user.last_name == 'User'
        assert user.check_password('newpassword123')
        assert not user.is_admin  # New users should not be admin
        assert user.active  # New users should be active
    
    def test_registration_duplicate_username(self, client, regular_user):
        """Test registration with duplicate username."""
        response = client.post('/auth/register', data={
            'username': regular_user.username,  # Existing username
            'email': 'different@example.com',
            'first_name': 'Different',
            'last_name': 'User',
            'password': 'password123',
            'password2': 'password123'  # Fixed field name
        })
        
        assert response.status_code == 200
        assert b'Please use a different username' in response.data
    
    def test_registration_duplicate_email(self, client, regular_user):
        """Test registration with duplicate email."""
        response = client.post('/auth/register', data={
            'username': 'differentuser',
            'email': regular_user.email,  # Existing email
            'first_name': 'Different',
            'last_name': 'User',
            'password': 'password123',
            'password2': 'password123'  # Fixed field name
        })
        
        assert response.status_code == 200
        assert b'Please use a different email address' in response.data
    
    def test_registration_password_mismatch(self, client):
        """Test registration with password mismatch."""
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'password123',
            'password2': 'differentpassword'  # Fixed field name
        })
        
        assert response.status_code == 200
        assert b'Passwords must match' in response.data


@pytest.mark.auth
class TestAuthenticationRequired:
    """Test routes that require authentication."""
    
    def test_dashboard_requires_login(self, client):
        """Test dashboard redirects to login when not authenticated."""
        response = client.get('/dashboard/')
        assert response.status_code == 302
        # Should redirect to login page
        assert '/auth/login' in response.location
    
    def test_admin_requires_login(self, client):
        """Test admin panel redirects to login when not authenticated."""
        response = client.get('/admin/')
        assert response.status_code == 302
        assert '/auth/login' in response.location
    
    def test_admin_requires_admin_role(self, logged_in_user):
        """Test admin panel requires admin role."""
        response = logged_in_user.get('/admin/', follow_redirects=True)
        assert response.status_code == 200
        # Check for access denied message
        access_denied = b'Access denied' in response.data
        admin_required = b'Administrator privileges required' in response.data
        assert access_denied or admin_required
    
    def test_admin_access_for_admin_user(self, logged_in_admin):
        """Test admin user can access admin panel."""
        response = logged_in_admin.get('/admin/')
        assert response.status_code == 200
        assert b'Admin Panel' in response.data or b'Dashboard' in response.data
