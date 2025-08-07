"""
Unit Tests for User Model
Tests for user creation, authentication, and model methods
"""

import pytest
from app.models.user import User, AuditLog
from app import db


class TestUserModel:
    """Test cases for User model."""
    
    def test_user_creation(self, app_context):
        """Test creating a new user."""
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpassword123'
        )
        
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.first_name == 'Test'
        assert user.last_name == 'User'
        assert user.password_hash is not None
        assert user.check_password('testpassword123')
        assert not user.check_password('wrongpassword')
    
    def test_password_hashing(self, app_context):
        """Test password hashing and verification."""
        user = User(
            username='testuser', 
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpassword123'
        )
        
        # Password hash should be set
        assert user.password_hash is not None
        
        # Should verify correct password
        assert user.check_password('testpassword123')
        
        # Should reject incorrect password
        assert not user.check_password('wrongpassword')
        
        # Hash should be different for same password
        user2 = User(
            username='testuser2', 
            email='test2@example.com',
            first_name='Test',
            last_name='User2',
            password='testpassword123'
        )
        assert user.password_hash != user2.password_hash
    
    def test_pam_user(self, app_context):
        """Test PAM user functionality."""
        user = User(
            username='pamuser',
            email='pam@example.com',
            first_name='PAM',
            last_name='User',
            use_pam_auth=True
        )
        
        # PAM users should not have password hash
        assert user.password_hash is None
        
        # PAM users should not use database password check
        assert not user.check_password('anypassword')
        
        # Note: PAM authentication testing requires system integration
    
    def test_user_properties(self, app_context):
        """Test user model properties."""
        user = User(
            username='propertiesuser',  # Unique username
            email='properties@example.com',  # Unique email
            first_name='Test',
            last_name='User',
            password='testpassword123',
            is_admin=True
        )
        
        # Add to session to activate SQLAlchemy defaults
        db.session.add(user)
        db.session.flush()  # Flush to get defaults without committing
        
        assert user.is_admin
        assert user.active  # Default is True from SQLAlchemy
        assert user.full_name == 'Test User'
        assert repr(user) == '<User propertiesuser>'
    
    def test_user_repr(self, app_context):
        """Test user string representation."""
        user = User(
            username='testuser', 
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpassword123'
        )
        assert repr(user) == '<User testuser>'


class TestAuditLog:
    """Test cases for AuditLog model."""
    
    def test_audit_log_creation(self, app_context, admin_user):
        """Test creating an audit log entry."""
        log = AuditLog.log_action(
            user_id=admin_user.id,
            action='test_action',
            resource_type='test_resource',
            resource_id='1',  # String to match model storage
            details='Test action performed',
            ip_address='127.0.0.1',
            user_agent='Test User Agent'
        )
        
        assert log.user_id == admin_user.id
        assert log.action == 'test_action'
        assert log.resource_type == 'test_resource'
        assert log.resource_id == '1'  # String comparison
        assert log.details == 'Test action performed'
        assert log.ip_address == '127.0.0.1'
        assert log.user_agent == 'Test User Agent'
        assert log.timestamp is not None
    
    def test_audit_log_user_relationship(self, app_context, admin_user):
        """Test audit log relationship with user."""
        log = AuditLog.log_action(
            user_id=admin_user.id,
            action='test_action',
            resource_type='test_resource',
            resource_id=1,
            details='Test action',
            ip_address='127.0.0.1',
            user_agent='Test User Agent'
        )
        
        # Test relationship
        assert log.user == admin_user
        assert log in admin_user.audit_logs
    
    def test_audit_log_repr(self, app_context, admin_user):
        """Test audit log string representation."""
        log = AuditLog.log_action(
            user_id=admin_user.id,
            action='test_action',
            resource_type='test_resource',
            resource_id='1',
            details='Test action',
            ip_address='127.0.0.1',
            user_agent='Test User Agent'
        )
        
        expected = f'<AuditLog test_action by User {admin_user.id}>'
        assert repr(log) == expected
