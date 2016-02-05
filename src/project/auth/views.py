from sqlalchemy import func
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask.ext.babel import gettext
from flask.ext.login import login_user, login_required, logout_user
from project import db, bcrypt, logger, login_manager
from project.toolbox.email import send_email_registration
from config import SEND_EMAIL_AFTER_REGISTRATION
from .forms import LoginForm, RegisterForm, ActivateForm
from .models import User
#from project.media.models import MediaFolder


mod_auth = Blueprint(
    'auth',
    __name__,
    url_prefix='/user',
    template_folder='templates'
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@mod_auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter(func.lower(User.username) == func.lower(form.username.data)).first()
            if user is not None and bcrypt.check_password_hash(
                user.password, form.password.data
            ):
                if not user.active:
                    logger.info('Login failed - user not active [' + user.username + '].')
                    flash(gettext('Your account is not activated.'))
                    return redirect(url_for('auth.activate'))
                login_user(user)
                logger.info('Login success - user login [' + user.username + '].')
                flash(gettext('You are logged in.'))
                return redirect(request.args.get('next') or url_for('index'))
            else:
                flash(gettext('Invalid username or password.'))
    return render_template('login.html', form=form)


@mod_auth.route('/logout')
@login_required
def logout():
    logout_user()
    logger.info('Logout success - user logout.')
    flash(gettext('You were logged out.'))
    return redirect(url_for('index'))


@mod_auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter(func.lower(User.username) == func.lower(form.username.data)).first()
        if user is None:
            user = User.query.filter(func.lower(User.email) == func.lower(form.email.data)).first()
            if user is None:
                # create new user
                user = User(
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data
                )
                db.session.add(user)
                db.session.commit()
                if SEND_EMAIL_AFTER_REGISTRATION:
                    send_email_registration(user)
                logger.info('Registration success - new user [' + form.username.data + '].')

                # create default media folder
                # mf = MediaFolder(foldername='default')
                # mf.rename = False
                # mf.author = user
                # db.session.add(mf)
                # db.session.commit()

                # activate user if need
                if not user.active:
                    flash(gettext('Your account is not activated.'))
                    return redirect(url_for('auth.activate'))
                login_user(user)
                return redirect(url_for('index'))
            else:
                logger.info('Registration failed - email address already in use. [' + form.email.data + '].')
                flash(gettext('This email address is already in use.'))
        else:
            logger.info('Registration failed - user name already in use. [' + form.username.data + '].')
            flash(gettext('This user name already in use.'))
    return render_template('register.html', form=form)


@mod_auth.route('/activate', methods=['GET', 'POST'])
@mod_auth.route('/activate/<code>', methods=['GET'])
def activate(code=None):
    form = ActivateForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            code = form.code.data
        else:
            logger.info('Activation failed - Invalid activation code.')
            flash(gettext('Invalid activation code.'))
    if code is not None:
        user = User.query.filter(func.lower(User.uuid) == func.lower(code)).first()
        if user is not None:
            user.active = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(gettext('Your account is activated.'))
            logger.info('Activation success - user [' + user.username + '].')
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('activate.html', form=form)


@mod_auth.route('/unsubscribe/<code>', methods=['GET'])
@login_required
def unsubscribe(code=None):
    user = User.query.filter(func.lower(User.uuid) == func.lower(code)).first()
    if user is not None:
        user.subscribed = False
        db.session.add(user)
        db.session.commit()
        logger.info('Unsubscribe success - user [' + user.username + '].')
        flash(gettext('You unsubscribed.'))
    return redirect(url_for('index'))


@mod_auth.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username=None):
    user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
    if user is not None:
        return render_template('profile.html', user=user)
    flash(gettext('User not found'))
    return redirect(url_for('index'))
