"""
Authentication Blueprint
User authentication routes and functionality for Lab Portal
"""

from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes  # noqa: F401,E402 - Route registration
