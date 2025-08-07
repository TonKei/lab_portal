"""
Dashboard Routes
Main dashboard interface routes for Lab Portal
"""

from flask import render_template
from flask_login import login_required, current_user

from app.dashboard import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """Main dashboard page"""
    return render_template('dashboard/index.html', title='Dashboard',
                           user=current_user)
