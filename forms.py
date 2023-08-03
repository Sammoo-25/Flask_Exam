from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import (
    InputRequired, Length, Email, EqualTo
)


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(message='Name is required.'),
                                           Length(min=2, max=50, message='Name must be between 2 and 50 characters.')])
    surname = StringField('Surname', validators=[InputRequired(message='Surname is required.'),
                                                 Length(min=2, max=50,
                                                        message='Surname must be between 2 and 50 characters.')])
    email = StringField('Email', validators=[Email()])

    password = PasswordField('Password', validators=[
        InputRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(message='Confirm Password is required.'),
                                                 EqualTo('password', message='Passwords do not match.')])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[
        InputRequired(message='Password is required.'),
        Length(min=8, message='Password must be at least 8 characters long.')
    ])