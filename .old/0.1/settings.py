# -*- coding: utf-8 -*-
import sys
import os.path as op

PROJECT_ROOT = op.dirname(op.realpath(__file__))
sys.path.insert(0, op.join(PROJECT_ROOT, 'apps'))

#DEBUG = True
#TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sergey Lagovskiy', 'slagovskiy@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3'
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Novosibirsk'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = op.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#if DEBUG:
#    STATIC_ROOT = ''
#else:
#    STATIC_ROOT = op.join(PROJECT_ROOT, 'static')
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    op.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # 3rd party middleware
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'mptt',

    # statistic
    'apps.statistic.middleware.StatisticMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    op.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # 'django.contrib.markup',

    # 3rd party libs
    # 'debug_toolbar',


    # project apps
    'utils',
    'apps.blog',
    'apps.banner',
    'apps.projects',
    'apps.about',
    'apps.admin',
    'apps.statistic',
    'apps.robot',
    'userprofile',
)

ALLOWED_HOSTS = [
    '*',
    #'.lagovskiy.com',
    #'.lagovskiy.com.',
]


try:
    from settings_local import *
except ImportError:
    pass

try:
    from config import *
except ImportError:
    pass

if not SECRET_KEY:
    raise Exception('You must provide SECRET_KEY value in settings_local.py')

AUTH_PROFILE_MODULE = 'userprofile.UserProfile'

INTERNAL_IPS = ('127.0.0.1',)

'''
Example for settings_local.py

import os.path as op
from settings import PROJECT_ROOT

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DB_PATH = op.join(PROJECT_ROOT, 'db')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DATABASE_NAME',
        'USER': 'USERNAME',
        'PASSWORD': 'PASSWORD',
        'HOST': '',
        'PORT': '',
        }
}

SECRET_KEY = '9@-a*+c1ms+25b6h836jkym=qs$mtd65i!aq4zd$b2o5(3mky+'

DOMAIN_NAME = 'http://qwertyuiop.com'

# email
DEFAULT_FROM_EMAIL = 'noreply@server.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.server.com'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'noreply@server.com'
EMAIL_HOST_PASSWORD = '123qwe'
EMAIL_SUBJECT_PREFIX = 'qwertyuiop.com'

# debug toolbar
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

def custom_show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'HIDE_DJANGO_SQL': False,
    'TAG': 'body',
    'ENABLE_STACKTRACES' : True,
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING_DATE_FORMAT_FULL = '%Y-%m-%d %H:%M:%S'
LOGGING_DATE_FORMAT_MINI = '%H:%M:%S'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'db': {
            'format' : "[%(asctime)s] %(levelname)s %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'request': {
            'format' : "[%(asctime)s] %(levelname)s %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'blog': {
            'format' : "[%(asctime)s] %(levelname)s %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'info': {
            'level': 'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': op.join(
                PROJECT_ROOT, op.join('logs', 'info.log')
                ),
            'when': 'midnight',
            'backupCount': 5,
            'formatter': 'verbose'
        },
        'db': {
            'level': 'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': op.join(
                PROJECT_ROOT, op.join('logs', 'db.log')
                ),
            'maxBytes': 1024*1024*10,
            'backupCount': 5,
            'formatter': 'db',
        },
        'request': {
            'level': 'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': op.join(
                PROJECT_ROOT, op.join('logs', 'request.log')
                ),
            'when': 'midnight',
            'backupCount': 15,
            'formatter': 'request',
        },
        'comment': {
            'level': 'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': op.join(
                PROJECT_ROOT, op.join('logs', 'comment.log')
                ),
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
            'formatter': 'blog',
        },
        'error': {
            'level': 'ERROR',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': op.join(
                PROJECT_ROOT, op.join('logs', 'error.log')
                ),
            'when': 'midnight',
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers':['info'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['db'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['request'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'blog.comment': {
            'handlers': ['comment'],
            'propagate': False,
            'level': 'DEBUG',
        },
        '': {
            'handlers': ['info', 'console', 'error'],
            'level': 'DEBUG',
        },
    }
}'''