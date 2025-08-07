"""
Test Configuration and Fixtures
Pytest configuration and shared fixtures for Lab Portal tests
"""

import pytest
from app import create_app, db
from app.models.user import User, AuditLog


@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for each test session."""
    
    # Create app with test configuration
    app = create_app('testing')
    
    # Create application context
    with app.app_context():
        db.create_all()
        yield app
        
        # Cleanup
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def app_context(app):
    """Create an application context for tests that need it."""
    with app.app_context():
        yield app


@pytest.fixture
def db_session(app_context):
    """Create a database session for tests."""
    # Create all tables
    db.create_all()
    
    yield db.session
    
    # Clean up - remove all data and close session
    db.session.remove()
    db.drop_all()


@pytest.fixture
def admin_user(app_context):
    """Create a test admin user."""
    # Clear any existing data first
    User.query.delete()
    AuditLog.query.delete()
    db.session.commit()
    
    user = User(
        username='testadmin',
        email='testadmin@example.com',
        first_name='Test',
        last_name='Admin',
        password='testpassword123',
        use_pam_auth=False,
        is_admin=True
    )
    
    db.session.add(user)
    db.session.commit()
    
    yield user
    
    # Cleanup
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception:
        db.session.rollback()


@pytest.fixture
def regular_user(app_context):
    """Create a test regular user."""
    # Clear any existing data first
    User.query.delete()
    AuditLog.query.delete()
    db.session.commit()
    
    user = User(
        username='testuser',
        email='testuser@example.com',
        first_name='Test',
        last_name='User',
        password='testpassword123',
        use_pam_auth=False,
        is_admin=False
    )
    
    db.session.add(user)
    db.session.commit()
    
    yield user
    
    # Cleanup
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception:
        db.session.rollback()


@pytest.fixture
def pam_user(app_context):
    """Create a test PAM user."""
    # Clear any existing data first
    User.query.delete()
    AuditLog.query.delete()
    db.session.commit()
    
    user = User(
        username='pamuser',
        email='pamuser@example.com',
        first_name='PAM',
        last_name='User',
        use_pam_auth=True,
        is_admin=True
    )
    # PAM users don't need password
    
    db.session.add(user)
    db.session.commit()
    
    yield user
    
    # Cleanup
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception:
        db.session.rollback()


@pytest.fixture
def logged_in_admin(client, admin_user):
    """Log in as admin user and return the client."""
    with client.session_transaction() as sess:
        sess['_user_id'] = str(admin_user.id)
        sess['_fresh'] = True
    return client


@pytest.fixture
def logged_in_user(client, regular_user):
    """Log in as regular user and return the client."""
    with client.session_transaction() as sess:
        sess['_user_id'] = str(regular_user.id)
        sess['_fresh'] = True
    return client


@pytest.fixture
def sample_audit_log(app_context, admin_user):
    """Create a sample audit log entry."""
    log = AuditLog.log_action(
        user_id=admin_user.id,
        action='test_action',
        resource_type='test_resource',
        resource_id=1,
        details='Test audit log entry',
        ip_address='127.0.0.1',
        user_agent='Test User Agent'
    )
    
    yield log
    
    # Cleanup handled by user fixture cleanup


# Helper functions for tests
def login_user(client, username, password):
    """Helper function to log in a user."""
    return client.post('/auth/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)


def logout_user(client):
    """Helper function to log out a user."""
    return client.get('/auth/logout', follow_redirects=True)


def create_test_user(username, email, password, is_admin=False,
                     use_pam_auth=False):
    """Helper function to create a test user."""
    # Clear existing users first
    User.query.filter_by(username=username).delete()
    User.query.filter_by(email=email).delete()
    db.session.commit()
    
    user = User(
        username=username,
        email=email,
        first_name='Test',
        last_name='User',
        password=password if not use_pam_auth else None,
        is_admin=is_admin,
        use_pam_auth=use_pam_auth
    )
    
    db.session.add(user)
    db.session.commit()
    
    return user