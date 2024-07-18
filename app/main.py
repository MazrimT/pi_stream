from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_apscheduler import APScheduler
import os
from app.lib.config import Config
from app.lib.overlay_downloader import download_overlay

# import views
from app.views.login import login_manager, login
from app.views.logout import logout
from app.views.index import index
from app.views.settings import settings


# set up the app
app = Flask(__name__)
app.secret_key = os.getenv("secret_key")
app.config["stream_config"] = Config()
bootstrap = Bootstrap5(app)
# makes sure we don't go online for bootstrap but uses servers files
app.config["BOOTSTRAP_SERVE_LOCAL"] = True

# To be able to test certain things on windows
app.config["PYTHON_EXECUTABLE"] = (
    f"{app.root_path}/../venv/Scripts/python.exe"
    if os.name == "nt"
    else f"{app.root_path}/../venv/bin/python"
)

# initiate login manager
login_manager.init_app(app)


# register views / blueprints
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(index)
app.register_blueprint(settings)

# set up appscheduler for the overlay downloader
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('interval', id='load_overlay', seconds=10, misfire_grace_time=900)
def load_overlay():
    download_overlay()
