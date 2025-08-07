#!/usr/bin/env python
"""
Lab Portal CLI Commands
Command-line utilities for Lab Portal management
"""

import click
from flask.cli import with_appcontext
from app import create_app, db
from app.models.user import User, AuditLog


@click.command()
@click.option('--username', prompt='Username', help='Admin username')
@click.option('--email', prompt='Email', help='Admin email address')
@click.option('--first-name', prompt='First name', help='First name')
@click.option('--last-name', prompt='Last name', help='Last name')
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True, help='Admin password')
@with_appcontext
def create_admin(username, email, first_name, last_name, password):
    """Create an admin user"""
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        click.echo(f'Error: User {username} already exists!')
        return
    
    if User.query.filter_by(email=email).first():
        click.echo(f'Error: Email {email} already exists!')
        return
    
    # Create admin user
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
        is_admin=True
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Log the admin creation
    AuditLog.log_action(
        user_id=user.id,
        action='admin_created',
        resource_type='user',
        details=f'Admin user created via CLI: {username}',
        ip_address='127.0.0.1',
        user_agent='CLI'
    )
    
    click.echo(f'Admin user {username} created successfully!')


@click.command()
@with_appcontext
def list_users():
    """List all users"""
    users = User.query.all()
    
    if not users:
        click.echo('No users found.')
        return
    
    click.echo('\nUsers:')
    click.echo('-' * 80)
    click.echo(f'{"ID":<4} {"Username":<20} {"Email":<30} '
               f'{"Name":<20} {"Admin":<6} {"Active":<6}')
    click.echo('-' * 80)
    
    for user in users:
        admin_status = 'Yes' if user.is_admin else 'No'
        active_status = 'Yes' if user.active else 'No'
        
        click.echo(f'{user.id:<4} {user.username:<20} {user.email:<30} '
                   f'{user.full_name:<20} {admin_status:<6} '
                   f'{active_status:<6}')
    
    click.echo(f'\nTotal users: {len(users)}')


@click.command()
@click.option('--username', prompt='Username', help='Username to deactivate')
@with_appcontext
def deactivate_user(username):
    """Deactivate a user account"""
    user = User.query.filter_by(username=username).first()
    
    if not user:
        click.echo(f'Error: User {username} not found!')
        return
    
    if not user.active:
        click.echo(f'User {username} is already deactivated.')
        return
    
    user.active = False
    db.session.commit()
    
    # Log the deactivation
    AuditLog.log_action(
        user_id=user.id,
        action='user_deactivated',
        resource_type='user',
        details=f'User deactivated via CLI: {username}',
        ip_address='127.0.0.1',
        user_agent='CLI'
    )
    
    click.echo(f'User {username} has been deactivated.')


@click.command()
@with_appcontext
def init_db():
    """Initialize the database with tables"""
    db.create_all()
    click.echo('Database tables created successfully!')


if __name__ == '__main__':
    app = create_app()
    
    # Register CLI commands
    app.cli.add_command(create_admin)
    app.cli.add_command(list_users)
    app.cli.add_command(deactivate_user)
    app.cli.add_command(init_db)
    
    with app.app_context():
        # You can call commands directly here if needed
        pass
