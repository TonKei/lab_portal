"""
Admin Blueprint
Administrative interface for Lab Portal
"""

from flask import Blueprint

bp = Blueprint('admin', __name__)

from app.admin import routes  # noqa
