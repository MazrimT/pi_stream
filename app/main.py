from flask import Flask, render_template, request, redirect, url_for
#from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_bootstrap import Bootstrap5
import os
import sys
from app.lib.config import Config

# import views
from app.views.login import login_manager, login
from app.views.logout import logout
from app.views.index import index
from app.views.settings import settings




# set up the app
app = Flask(__name__)
app.secret_key = os.getenv('secret_key')
app.config["stream_config"] = Config(app_path=app.root_path)
bootstrap = Bootstrap5(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True      # makes sure we don't go online for bootstrap but uses servers files

# To be able to test certain things on windows
app.config["PYTHON_EXECUTABLE"] = f"{app.root_path}/../venv/Scripts/python.exe" if os.name == "nt" else f"{app.root_path}/../venv/bin/python"

# initiate login manager
login_manager.init_app(app)


# register views / blueprints
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(index)
app.register_blueprint(settings)


