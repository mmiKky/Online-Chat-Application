from flask import render_template
from online_chat_app import app
from online_chat_app.forms import RegisterForm, LoginForm

PAGE_TITLE = 'ChatBox'
COLOR = '#08d8db'


@app.route('/')
def welcome_page():
    return render_template('welcome.html', page_title=PAGE_TITLE, color=COLOR)


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/login')
def login_page():
    form = LoginForm()
    return render_template('login.html', page_title=PAGE_TITLE, color=COLOR, form=form)


@app.route('/registration')
def registration_page():
    form = RegisterForm()
    return render_template('register.html', page_title=PAGE_TITLE, color=COLOR, form=form)
