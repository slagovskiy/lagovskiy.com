import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = None
CSRF_ENABLED = True

# SQLALCHEMY
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'base.sqlite') moved to config_local
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')

# WHOOSH
WHOOSH_BASE = os.path.join(basedir, 'db_search')
MAX_SEARCH_RESULTS = 50

# BABEL
LANGUAGES = {
    'en': 'English',
    'ru': 'Russian'
}

#CAPTCHA
CAPTCHA_FONT_PATH = os.path.normpath(
    os.path.join(os.path.join(basedir, 'fonts'), 'sketch_2.ttf'))
CAPTCHA_FONT_SIZE = 42
CAPTCHA_LETTER_ROTATION_LEFT = -35
CAPTCHA_LETTER_ROTATION_RIGHT = 35
CAPTCHA_CHARS = 'QWERTYUIPASDFGHJKLZXCVBNM123456789@#$%'
CAPTCHA_COLORS = ['#00267C', '#AF0000', '#3400C4', '#005089', '#347F3D',
                  '#CE9300', '#282828', '#580082', '#008E8E', '#A84300']

UPLOAD_DIR = os.path.join(basedir, 'uploads')

try:
    from config_local import *
except ImportError:
    pass

if SECRET_KEY is None:
    raise Exception('You must provide SECRET_KEY value in config_local.py')

'''
Example: config_local.py:

import os
from config import basedir

debug=True

SITE_NAME = 'lagovskiy.com'

SECRET_KEY = 'QWerTYuiOP245'

# MAIL CONFIG
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'admin'
MAIL_PASSWORD = 'admin'

ADMINS = ['admin@localhost.local']

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'base.sqlite')

#LOG
WRITE_LOG_FILE = True

#USER
USER_MUST_ACTIVATE_REGISTRATION = False
'''
