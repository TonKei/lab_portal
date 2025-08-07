"""
Lab Portal Configuration
Centralized configuration management for the Lab Portal Management System
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class"""
    
    # Flask Core Settings
    SECRET_KEY = (os.environ.get('SECRET_KEY') or
                  'dev-secret-key-change-in-production')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               'sqlite:///lab_portal.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Security Settings
    BCRYPT_LOG_ROUNDS = int(os.environ.get('BCRYPT_LOG_ROUNDS', 12))
    PERMANENT_SESSION_LIFETIME = timedelta(
        days=int(os.environ.get('TOKEN_EXPIRATION_DAYS', 7)),
        seconds=int(os.environ.get('TOKEN_EXPIRATION_SECONDS', 0))
    )
    
    # Lab Network Configuration
    LAB_NETWORK_RANGE = os.environ.get('LAB_NETWORK_RANGE', '192.168.1.0/24')
    DHCP_SERVER_IP = os.environ.get('DHCP_SERVER_IP', '192.168.1.1')
    DEFAULT_GATEWAY = os.environ.get('DEFAULT_GATEWAY', '192.168.1.1')
    DNS_SERVERS = os.environ.get('DNS_SERVERS', '8.8.8.8,8.8.4.4').split(',')
    
    # PAM Authentication
    PAM_SERVICE = os.environ.get('PAM_SERVICE', 'login')
    ENABLE_PAM_AUTH = (os.environ.get('ENABLE_PAM_AUTH', 'true').lower() ==
                       'true')
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = (os.environ.get('RATELIMIT_STORAGE_URL',
                                            'memory://'))
    RATELIMIT_ENABLED = (os.environ.get('RATELIMIT_ENABLED', 'true').lower()
                         == 'true')
    
    # WTF Forms
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # File Upload Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    UPLOAD_FOLDER = 'uploads'
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/lab_portal.log')
    
    # Application Features
    FEATURES = {
        'dhcp_management': True,
        'device_discovery': True,
        'network_monitoring': True,
        'user_management': True,
        'audit_logging': True,
        'real_time_updates': True
    }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # Development Database (SQLite)
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               'sqlite:///lab_portal_dev.db')
    
    # Relaxed security for development
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False  # Disable CSRF for API testing
    
    # Development logging
    LOG_LEVEL = 'DEBUG'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
    # In-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Minimal security for testing
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    
    # Disable rate limiting for testing
    RATELIMIT_ENABLED = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Production Database (PostgreSQL)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://lab_portal:password@localhost/lab_portal'
    
    # Enhanced security for production
    BCRYPT_LOG_ROUNDS = 15
    WTF_CSRF_ENABLED = True
    
    # Production logging
    LOG_LEVEL = 'WARNING'
    
    # Production rate limiting
    RATELIMIT_STORAGE_URL = 'redis://localhost:6379'


# Configuration selector
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get the appropriate configuration based on environment"""
    return config[os.environ.get('FLASK_ENV', 'default')]
