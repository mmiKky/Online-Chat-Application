from database import db, bcrypt, login_manager
from flask_login import UserMixin


# reloads user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
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


# class Friends(db.Model):
#     id = db.Colum(db.Integer())
