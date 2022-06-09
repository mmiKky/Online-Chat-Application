from datetime import datetime

from database import db
from database.models import User, Friends, Message


class DatabaseManager:
    # creates tables that don't exist yet
    db.create_all()

    @staticmethod
    def add_user(username, email, password):
        user = User(username=username,
                    email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def add_friend(current_user, user_friend):
        # user doesn't have a relation with other user
        if not DatabaseManager.check_if_friends(current_user.username, user_friend.username):
            friend = Friends(user_id=current_user.id,
                             friend_id=user_friend.id)
            db.session.add(friend)
            db.session.commit()

    @staticmethod
    def get_friends_list(current_user):
        friends = Friends.query.filter_by(user_id=current_user.id).all()

        # find friends usernames and add to the list; 1st user id in Friends table
        friends_list = []
        for friend in friends:
            friend = User.query.filter_by(id=friend.friend_id).first()
            friends_list.append(friend.username)

        friends = Friends.query.filter_by(friend_id=current_user.id).all()

        # find friends usernames and add to the list; 2nd user id in Friends table
        for friend in friends:
            friend = User.query.filter_by(id=friend.user_id).first()
            friends_list.append(friend.username)

        friends_list.sort()
        return friends_list

    @staticmethod
    def check_if_friends(current_username, friend_username):
        # get users from database
        user = User.query.filter_by(username=current_username).first()
        friend = User.query.filter_by(username=friend_username).first()
        if not user or not friend:
            return False
        # check if those users are connected in Friends table; for both positions
        friends = Friends.query.filter_by(user_id=user.id, friend_id=friend.id).first()  # it gives an object
        if not friends:
            friends = Friends.query.filter_by(user_id=friend.id, friend_id=user.id).first()

        if friends:
            return True
        else:
            return False

    @staticmethod
    def check_if_username_exists(username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            return True
        else:
            return False

    @staticmethod
    def check_if_email_exists(email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            return True
        else:
            return False

    @staticmethod
    def get_room_id(current_username, friend_username):
        # get users from database
        current_user = DatabaseManager.username_to_user(current_username)
        friend_user = DatabaseManager.username_to_user(friend_username)

        # check if those users are connected; if so, get room_id
        friends = Friends.query.filter_by(user_id=current_user.id, friend_id=friend_user.id).first()
        if friends:
            return friends.room_id
        friends = Friends.query.filter_by(user_id=friend_user.id, friend_id=current_user.id).first()
        if friends:
            return friends.room_id
        else:
            return None

    @staticmethod
    # get message from database for particular conversation
    def get_messages(current_username, friend_username):
        # get users from database
        current_user = DatabaseManager.username_to_user(current_username)
        friend_user = DatabaseManager.username_to_user(friend_username)
        if not current_user or not friend_user:
            return []

        # get messages for the right one room_id
        messages_list = []
        room_id = DatabaseManager.get_room_id(current_username, friend_username)
        if room_id is not None:
            messages = Message.query.filter_by(room_id=room_id).all()

            # make data iterable
            messages_iter = []
            for mess in messages:
                messages_iter.append((mess.id, mess.author, mess.content, mess.date))
            # sort by date
            for mess in sorted(messages_iter, key=lambda x: x[0], reverse=False)[:]:
                id, author, content, date = mess
                messages_list.append({'name': DatabaseManager.user_id_to_username(author), 'message': content, 'date': date})
        return messages_list

    @staticmethod
    def save_message(current_username, room_id, message):
        message = Message(room_id=room_id,
                          author=DatabaseManager.username_to_user(current_username).id,
                          content=message,
                          date=datetime.now())
        db.session.add(message)
        db.session.commit()

    @staticmethod
    def username_to_user(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def user_id_to_username(user_id):
        return User.query.filter_by(id=user_id).first().username
