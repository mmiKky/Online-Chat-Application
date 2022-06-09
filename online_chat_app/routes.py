import flask_login
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required
from flask_socketio import SocketIO, join_room, leave_room, emit

import online_chat_app
from online_chat_app import app
from online_chat_app import socketio
from online_chat_app.forms import RegisterForm, LoginForm, SearchFriendForm
from database.models import User

PAGE_TITLE = 'ChatBox'
COLOR = '#08d8db'


@app.route('/')
def welcome_page():
    return render_template('welcome.html', page_title=PAGE_TITLE, color=COLOR)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home_page():
    user_friends = online_chat_app.get_database_manager().get_friends_list(flask_login.current_user)
    return render_template('home.html', page_title=PAGE_TITLE, users=user_friends)


@app.route('/home_chat', methods=['GET', 'POST'])
@login_required
def home_page_chat():
    if request.method == 'POST':
        selected = request.form.get('user')
        session['username'] = flask_login.current_user.username
        session['room'] = online_chat_app.get_database_manager().get_room_id(flask_login.current_user.username, selected)
        print(flask_login.current_user.username)
        print(online_chat_app.get_database_manager().get_messages(flask_login.current_user.username, selected))
        return render_template('home_chat.html', page_title=PAGE_TITLE, username=selected, session=session)
    else:
        if session.get('username') is not None:
            return render_template('chat.html', session = session)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search_friend_page():
    form = SearchFriendForm()

    if form.validate_on_submit():
        user_friend = User.query.filter_by(username=form.username.data).first()

        if user_friend:
            if user_friend.username != flask_login.current_user.username:
                database_manager = online_chat_app.get_database_manager()
                database_manager.add_friend(flask_login.current_user, user_friend)
                flash(f'User {user_friend.username} added to the friends list.', category='success')
                return redirect(url_for('home_page'))
            else:
                flash(f'You are searching for yourself.', category='info')
        else:
            flash('User does not exists. Please make sure you typed user name correctly.', category='danger')
    if form.errors != {}:   # some errors occurred
        for err_msg in form.errors.values():
            flash(f'Error occurred while searching user: {err_msg}', category='info')
    return render_template('search_friend.html', page_title=PAGE_TITLE, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login_form = LoginForm()

    # check if user exists in database; if exists check password
    if login_form.validate_on_submit():
        user_to_login = User.query.filter_by(username=login_form.username.data).first()
        if user_to_login and user_to_login.check_password(login_form.password.data):
            login_user(user_to_login)
            flash(f'Logged in successfully as {user_to_login.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username or password incorrect. Please try again.', category='danger')

    return render_template('login.html', page_title=PAGE_TITLE, color=COLOR, form=login_form)


@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    reg_form = RegisterForm()
    # check if user exists in database; if it doesn't exist create new account
    if reg_form.validate_on_submit():
        database_manager = online_chat_app.get_database_manager()
        database_manager.add_user(username=reg_form.username.data,
                                  email=reg_form.email_address.data,
                                  password=reg_form.password1.data)
        return redirect(url_for('login_page'))
    if reg_form.errors != {}:   # some errors occurred
        for err_msg in reg_form.errors.values():
            flash(f'Error occurred while creating new user: {err_msg}', category='danger')

    return render_template('register.html', page_title=PAGE_TITLE, color=COLOR, form=reg_form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('Log out successfully.', category='info')
    return redirect(url_for('login_page'))


@socketio.on('join', namespace='/home_chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/home_chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


@socketio.on('left', namespace='/home_chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)




# # server-side event handler
# @socketio.on('my event')
# def handle_my_event(data):
#     print('received message: ' + str(data))



