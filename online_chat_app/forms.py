import flask_login
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from database.models import User
import online_chat_app

MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 30


# represents registration panel; contains constraints
class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()     # it gives an object
        if user:
            raise ValidationError('User with that user name already exists. Please try different user name.')

    def validate_email_address(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()       # it gives an object
        if user:
            raise ValidationError('User with that email address already exists. Please try different email address.')

    username = StringField(label='User Name:', validators=[Length(min=MIN_USERNAME_LENGTH, max=MAX_USERNAME_LENGTH),
                                                           DataRequired()])
    email_address = StringField(label='Email address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=5), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])  # confirm password
    submit = SubmitField(label='Create Account')


# represent log in panel; contains constraints
class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Log in')


# represent search user form; contains constraints
class SearchFriendForm(FlaskForm):

    def validate_username(self, username_to_check):
        if online_chat_app.get_database_manager().check_if_friends(flask_login.current_user.username, username_to_check.data):
            raise ValidationError('You are friends already.')

    username = StringField(label='User Name:', validators=[Length(min=MIN_USERNAME_LENGTH, max=MAX_USERNAME_LENGTH),
                                                           DataRequired()])
    submit = SubmitField(label='Search')
