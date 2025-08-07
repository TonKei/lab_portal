"""
Authentication Routes
Login, logout, and user management routes for Lab Portal
"""

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse

from app import db, limiter
from app.auth import bp
from app.models.user import User, AuditLog
from app.auth.forms import LoginForm, RegistrationForm


@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Your account has been deactivated. '
                      'Please contact an administrator.', 'error')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=form.remember_me.data)
            user.update_last_login()
            
            # Log successful login
            AuditLog.log_action(
                user_id=user.id,
                action='login',
                resource_type='authentication',
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string
            )
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('dashboard.index')
            
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(next_page)
        else:
            # Log failed login attempt
            if user:
                AuditLog.log_action(
                    user_id=user.id,
                    action='login_failed',
                    resource_type='authentication',
                    details='Invalid password',
                    ip_address=request.remote_addr,
                    user_agent=request.user_agent.string
                )
            
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
@login_required
def logout():
    """User logout route"""
    # Log logout action
    AuditLog.log_action(
        user_id=current_user.id,
        action='logout',
        resource_type='authentication',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("3 per hour")
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if this is the first user (make them admin)
        user_count = User.query.count()
        is_first_user = user_count == 0
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
            is_admin=is_first_user
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Log user registration
        AuditLog.log_action(
            user_id=user.id,
            action='register',
            resource_type='user',
            details=f'New user registered: {user.username}',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        
        admin_msg = ("You have been granted administrator privileges "
                     "as the first user." if is_first_user else "")
        flash(f'Registration successful! {admin_msg}', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('auth/profile.html', title='Profile',
                           user=current_user)


@bp.route('/api/auth/status')
def auth_status():
    """API endpoint to check authentication status"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'full_name': current_user.full_name,
                'is_admin': current_user.is_admin
            }
        })
    else:
        return jsonify({'authenticated': False})
