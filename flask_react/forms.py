# pip install flask-wtf
# pip install email_validator

# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from flask_react.models import User
from flask_wtf.file import FileField, FileAllowed, FileRequired


# Classes that repreasent our forms in python
class RegistrationForm(FlaskForm):
    # Allow Username from 2 chars to 20 chars
    first_name = StringField(
        'First_Name',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    middle_name = StringField(
        'Middle_Name',
        validators=[
            Length(min=2, max=20)
        ]
    )
    last_name = StringField(
        'Last_Name',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    date = DateField(
        'Date',
        format= '%Y-%m-%d'
        )
    
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
    )
    
    profile_image = FileField(
        'Profile Image', 
        validators=[
            FileAllowed(['jpeg', 'jpg', 'png'], 'only images are allowed' ), 
            FileRequired('File Field shoud not be empty')]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField(
        'Sign Up'
    )

    # custom validaion functions 
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is taken")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("emial is taken")


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField(
        'Login'
    )

class PostForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired(),
            Length(min=2, max=20)
        ]
        )

    content = TextAreaField(
        'Post Content',
        validators=[
            DataRequired()
        ]
        )
    
    status = SelectField(u'Share with', 
                        choices=[('Public', 'Public'), ('Friends_only', 'Friends_only'), ('Only_me', 'Only_me')]
        )
    submit = SubmitField(
        'Add Post'
    )
    