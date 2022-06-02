from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    username = StringField(label='User Name:')
    email_address = StringField(label='Email address:')
    password1 = PasswordField(label='Password:')
    password2 = PasswordField(label='Confirm Password:')    # confirm password
    submit = SubmitField(label='Submit')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:')
    password = PasswordField(label='Password:')
    submit = SubmitField(label='Submit')
