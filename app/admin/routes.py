"""
Admin Routes
Administrative interface routes for Lab Portal
"""

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps

from app import db
from app.admin import bp
from app.models.user import User, AuditLog


def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied. Administrator privileges required.', 'error')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard"""
    # Get basic statistics
    total_users = User.query.count()
    active_users = User.query.filter_by(active=True).count()
    admin_users = User.query.filter_by(is_admin=True).count()
    
    # Get recent audit logs
    recent_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(10).all()
    
    return render_template('admin/index.html', 
                           title='Admin Panel',
                           total_users=total_users,
                           active_users=active_users,
                           admin_users=admin_users,
                           recent_logs=recent_logs)


@bp.route('/users')
@login_required
@admin_required
def users():
    """User management"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', 
                           title='User Management',
                           users=users)


@bp.route('/users/<int:user_id>/toggle')
@login_required
@admin_required
def toggle_user(user_id):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot deactivate your own account.', 'error')
        return redirect(url_for('admin.users'))
    
    user.active = not user.active
    db.session.commit()
    
    action = 'activated' if user.active else 'deactivated'
    flash(f'User {user.username} has been {action}.', 'success')
    
    # Log the action
    AuditLog.log_action(
        user_id=current_user.id,
        action=f'user_{action}',
        resource_type='user',
        resource_id=user.id,
        details=f'User {user.username} {action} by {current_user.username}',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    
    return redirect(url_for('admin.users'))


@bp.route('/users/<int:user_id>/toggle_pam')
@login_required
@admin_required
def toggle_pam(user_id):
    """Toggle PAM authentication for a user"""
    user = User.query.get_or_404(user_id)
    
    user.use_pam_auth = not user.use_pam_auth
    db.session.commit()
    
    auth_type = 'PAM' if user.use_pam_auth else 'Database'
    flash(f'User {user.username} authentication changed to {auth_type}.', 'success')
    
    # Log the action
    AuditLog.log_action(
        user_id=current_user.id,
        action=f'pam_{"enabled" if user.use_pam_auth else "disabled"}',
        resource_type='user',
        resource_id=user.id,
        details=f'PAM authentication {"enabled" if user.use_pam_auth else "disabled"} for {user.username}',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    
    return redirect(url_for('admin.users'))


@bp.route('/logs')
@login_required
@admin_required
def logs():
    """Audit log viewer"""
    page = request.args.get('page', 1, type=int)
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    return render_template('admin/logs.html',
                           title='Audit Logs',
                           logs=logs)
