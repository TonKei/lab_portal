"""
Lab Portal Application Entry Point
Flask application startup for Lab Portal Management System
"""

from dotenv import load_dotenv

from app import create_app, db
from app.models.user import User, AuditLog

# Load environment variables
load_dotenv()

# Create Flask application
app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Make database models available in flask shell"""
    return {
        'db': db,
        'User': User,
        'AuditLog': AuditLog
    }


@app.cli.command()
def init_db():
    """Initialize the database with tables"""
    db.create_all()
    print('Database tables created successfully.')


@app.cli.command()
def create_admin():
    """Create an administrative user"""
    import getpass
    
    username = input('Admin username: ')
    email = input('Admin email: ')
    first_name = input('First name: ')
    last_name = input('Last name: ')
    password = getpass.getpass('Password: ')
    
    try:
        admin_user = User.create_admin_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        print(f'Administrator user "{admin_user.username}" '
              f'created successfully.')
    except Exception as e:
        print(f'Error creating admin user: {e}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
