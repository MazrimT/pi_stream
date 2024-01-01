from flask import Blueprint, request, redirect, render_template, url_for
from flask_login import LoginManager, UserMixin, login_user
import os

login = Blueprint('login', __name__)
login_manager = LoginManager()

class User(UserMixin):
    """ User class for the login manager """
    pass

users = {os.getenv('user'): {'password': os.getenv('password')}}

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login.login'))


@login.route('/login', methods=['GET', 'POST'], endpoint='login')
def v_login():
    
    if request.method == 'GET':
        return render_template(
            'login.html'
        )
    
    email = request.form['email']
    if email in users and request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for('index.index'))

    return redirect(url_for('login.login'))

