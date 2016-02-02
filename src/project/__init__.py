import os
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from flask import Flask
from flask.ext.mail import Mail
from flask.ext.babel import Babel
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from config import basedir, WRITE_LOG_FILE


app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)

babel = Babel(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'auth.login'

bcrypt = Bcrypt(app)

logger = app.logger

#from project.XXX.views import mod_XXX

#app.register_blueprint(mod_XXX)

if WRITE_LOG_FILE:
    logdir = os.path.join(basedir, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    app.logger.setLevel(logging.INFO)

    logfile = os.path.join(logdir, 'main')
    file_handler = RotatingFileHandler(logfile, 'a', 1 * 1024 * 1024, 30)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    logfile = os.path.join(logdir, 'error')
    file_handler = TimedRotatingFileHandler(logfile, 'd', 1, 30)
    file_handler.setFormatter(logging.Formatter('\n\n%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]\n\n'))
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)

app.logger.info('app startup')

from project import views, models
