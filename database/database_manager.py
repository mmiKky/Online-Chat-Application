from database import db


class DatabaseManager:

    def __init__(self):
        db.create_all()

    @staticmethod
    def add_user(user):
        db.session.add(user)
        db.session.commmit()
