from flask import Flask
from flask_socketio import SocketIO
from flask_session import Session


app = Flask(__name__)

app.config['SECRET_KEY'] = '00a5a42de56abb02e4e0c3ca'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)
socketio = SocketIO(app)

import online_chat_app.routes


# to avoid circular importing, database manager is acquired using method
def get_database_manager():
    import database.database_manager
    database_manager = database.database_manager.DatabaseManager()
    return database_manager
