"""
Main Routes
Core application routes for Lab Portal
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Home page - redirect to dashboard if authenticated, login otherwise"""
    return redirect(url_for('auth.login'))


@bp.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return {'status': 'healthy', 'service': 'lab_portal'}, 200


@bp.route('/about')
def about():
    """About page with system information"""
    return render_template('about.html', title='About')


@bp.route('/help')
@login_required
def help():
    """Help and documentation page"""
    return render_template('help.html', title='Help')
