from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, FloatField
from wtforms.validators import (
    InputRequired, Length, Email, EqualTo, DataRequired, Regexp
)


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(message='Name is required.'),
                                           Length(min=2, max=50, message='Name must be between 2 and 50 characters.')])
    surname = StringField('Surname', validators=[InputRequired(message='Surname is required.'),
                                                 Length(min=2, max=50,
                                                        message='Surname must be between 2 and 50 characters.')])
    email = StringField('Email', validators=[Email()])

    gender = StringField('Gender', validators=[
        InputRequired(message='Gender is required.'),
        Regexp('^M|F$', message='Gender must be either "M" or "F".')])
    phone_number = StringField('Phone Number', validators=[InputRequired(message='Phone Number is required.')])

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


class UpdateProfileImageForm(FlaskForm):
    profile_image = FileField('Update Profile Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload')


# class UpdateProductImageForm(FlaskForm):
#     image = FileField('Update Product Image', validators=[FileAllowed(['jpg', 'png'])])
#     submit = SubmitField('Upload')


class AddProductForm(FlaskForm):
    ProductName = StringField('Product Name', validators=[InputRequired(message='Product Name is required.'),
                                                          Length(min=2, max=80,
                                                                 message='Name must be between 2 and 80 characters.')])
    Description = StringField('Description', validators=[InputRequired(message='Description is required.'),
                                                         Length(min=2, max=150,
                                                                message='Description must be between 2 and 150 characters.')])
    category = SelectField("Category", choices=[
        ('1', 'New Arrival'),
        ('2', 'Most Popular'),
        ('3', 'Trending')
    ], validators=[DataRequired()])
    expire_date = DateField("Expire Date", format="%Y-%m-%d", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    image = FileField("Product Image")

