from database import db
from database.models import User


class DatabaseManager:

    def __init__(self):
        db.create_all()

    # @staticmethod
    # def add_user(user):
    #     db.session.add(user)
    #     db.session.commit()

    @staticmethod
    def add_user(username, email, password):
        user = User(username=username,
                    email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()
