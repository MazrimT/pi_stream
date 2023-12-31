from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap5
import json
from pathlib import Path
from dotenv import load_dotenv
import os
from .lib.config import Config

load_dotenv(dotenv_path="../.env")

app = Flask(__name__)
app.secret_key = os.getenv('secret_key')
app.config["stream_config"] = Config(app_path=app.root_path)

bootstrap = Bootstrap5(app)

# Add all views here
views = ['index']

# import all views
for view in views: globals()[view] = getattr(__import__(f"app.views.{view}", fromlist=[view]), view)

# register blueprints for all views the views in the app
[app.register_blueprint(globals()[view]) for view in views]


app.config['BOOTSTRAP_SERVE_LOCAL'] = True      # makes sure we don't go online for bootstrap but uses servers files


# login stuff
users = {os.getenv('user'): {'password': os.getenv('password')}}

## setup login manager
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    pass

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = request.form['email']
    if email in users and request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'

@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.id

@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401