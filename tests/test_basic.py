"""
Basic Application Tests
Tests for basic application functionality and routes
"""

import pytest


class TestBasicRoutes:
    """Test basic application routes."""
    
    def test_app_creation(self, app):
        """Test that app is created correctly."""
        assert app is not None
        assert app.config['TESTING'] is True
    
    def test_home_redirect(self, client):
        """Test that home page redirects appropriately."""
        response = client.get('/')
        # Should redirect somewhere (login, dashboard, or landing page)
        assert response.status_code in [200, 302]
    
    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent-page')
        assert response.status_code == 404


class TestApplicationContext:
    """Test application context and configuration."""
    
    def test_app_config(self, app):
        """Test application configuration."""
        assert app.config['TESTING'] is True
        assert app.config['WTF_CSRF_ENABLED'] is False
        assert 'SECRET_KEY' in app.config
    
    def test_database_connection(self, app_context):
        """Test database connection in app context."""
        from app import db
        # Should be able to access database
        assert db is not None
        # Database should be accessible
        with app_context.app_context():
            # This should not raise an exception
            result = db.session.execute(db.text('SELECT 1'))
            assert result is not None


class TestHelperFunctions:
    """Test helper functions from conftest."""
    
    def test_login_helper(self, client, regular_user):
        """Test login helper function."""
        from tests.conftest import login_user
        
        response = login_user(client, regular_user.username, 'testpassword123')
        assert response.status_code == 200
    
    def test_logout_helper(self, logged_in_user):
        """Test logout helper function."""
        from tests.conftest import logout_user
        
        response = logout_user(logged_in_user)
        assert response.status_code == 200
    
    def test_create_test_user_helper(self, app_context):
        """Test create test user helper function."""
        from tests.conftest import create_test_user
        from app.models.user import User
        
        user = create_test_user(
            username='helpertest',
            email='helper@example.com',
            password='testpass123'
        )
        
        assert isinstance(user, User)
        assert user.username == 'helpertest'
        assert user.email == 'helper@example.com'
        assert user.check_password('testpass123')
