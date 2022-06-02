from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '00a5a42de56abb02e4e0c3ca'


import online_chat_app.routes
