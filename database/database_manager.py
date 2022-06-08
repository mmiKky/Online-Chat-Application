from database import db
from database.models import User, Friends


class DatabaseManager:
    db.create_all()
    # def __init__(self):
    #     db.create_all()

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

    @staticmethod
    def add_friend(current_user, user_friend):
        friend = Friends(user_id=current_user.id,
                         friend_id=user_friend.id,
                         message='')

        db.session.add(friend)
        db.session.commit()

    @staticmethod
    def check_if_friends(current_username, friend_username):
        user = User.query.filter_by(username=current_username).first()
        friend = User.query.filter_by(username=friend_username).first()
        if not user or not friend:
            return False
        friends = Friends.query.filter_by(user_id=user.id, friend_id=friend.id).first()  # it gives an object

        if friends:
            return True
        else:
            return False
