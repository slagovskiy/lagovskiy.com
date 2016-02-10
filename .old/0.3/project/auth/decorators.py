from functools import wraps
from flask.ext.login import current_user
from flask.ext.babel import gettext
from flask import request, flash, url_for, redirect
from .config import ROLE_ADMIN, ROLE_STAFF


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash(gettext('You need to be signed in for this page.'))
            return redirect(url_for('auth.login', next=request.path))
        return func(*args, **kwargs)
    return decorated_view


def role_admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash(gettext('You need to be signed in for this page.'))
            return redirect(url_for('auth.login', next=request.path))
        else:
            if not current_user.role <= ROLE_ADMIN:
                flash(gettext('You need to be admin for this page.'))
                return redirect(url_for('auth.login', next=request.path))
            else:
                return func(*args, **kwargs)
    return decorated_view


def role_staff_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            flash(gettext('You need to be signed in for this page.'))
            return redirect(url_for('auth.login', next=request.path))
        else:
            if not current_user.role <= ROLE_STAFF:
                flash(gettext('You need to be staff for this page.'))
                return redirect(url_for('auth.login', next=request.path))
            else:
                return func(*args, **kwargs)
    return decorated_view
