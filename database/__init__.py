"""This module separates database from the app logic"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from online_chat_app import app


app.config['SQLALCHEMY_DATA_BASE_URI'] = 'sqlite:///../database/online_chat.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)    # encrypts passwords in database
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'     # set log in page
login_manager.login_message = u'Zaloguj sie aby uzyskac dostep'     # message for non-logged in user
