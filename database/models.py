from database import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime


# reloads user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# those three classes represents tables in database
# UserMixin provides default implementations of methods required to implement user
class User(db.Model, UserMixin):
    """
    stores information about user and hashes passwords
    """
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    hashed_password = db.Column(db.String(length=1000), nullable=False)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, plain_text_password):
        self.hashed_password = bcrypt.generate_password_hash(plain_text_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)


class Friends(db.Model):
    """
    -stores information about user's relations
    -if two users are friends database contains 1, 3 for example, but not 3, 1
    -each pair of users that are friends has a room id, which is a primary key
    -user can't be a friend to itself
    """
    room_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)


class Message(db.Model):
    """
    stores information about messages send between users;
    room_id - defines between which users this conversation was
    """
    id = db.Column(db.Integer(), primary_key=True)
    room_id = db.Column(db.Integer(), db.ForeignKey('friends.room_id'), nullable=False)
    author = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String())
    date = db.Column(db.DateTime(), default=datetime.now())
