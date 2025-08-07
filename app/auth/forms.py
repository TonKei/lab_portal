"""
Authentication Forms
WTForms for user authentication in Lab Portal
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from app.models.user import User


class LoginForm(FlaskForm):
    """Login form for user authentication"""
    
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80)
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """Registration form for new users"""
    
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ])
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username is already taken"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        """Check if email is already registered"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ChangePasswordForm(FlaskForm):
    """Form for changing user password"""
    
    current_password = PasswordField('Current Password', validators=[
        DataRequired()
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired()
    ])
    new_password2 = PasswordField('Repeat New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')


class ProfileUpdateForm(FlaskForm):
    """Form for updating user profile information"""
    
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ])
    submit = SubmitField('Update Profile')
    
    def __init__(self, original_email, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
    
    def validate_email(self, email):
        """Check if email is already registered by another user"""
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')
