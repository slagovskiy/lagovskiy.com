from flask.ext.babel import gettext
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from .config import SIZE_USERNAME, SIZE_PASSWORD, SIZE_EMAIL, SIZE_UUID


class LoginForm(Form):
    username = StringField(gettext('Username'), [DataRequired(), Length(min=3, max=SIZE_USERNAME)])
    password = PasswordField(gettext('Password'), [DataRequired(), Length(min=3, max=SIZE_PASSWORD)])


class RegisterForm(Form):
    username = StringField(gettext('Username'), [DataRequired(), Length(min=3, max=SIZE_USERNAME)])
    email = StringField(gettext('Email address'), [DataRequired(), Email(), Length(min=3, max=SIZE_EMAIL)])
    password = PasswordField(gettext('Password'), [DataRequired(), Length(min=3, max=SIZE_PASSWORD)])
    confirm = PasswordField(gettext('Repeat Password'), [
        DataRequired(),
        EqualTo('password', message=gettext('Passwords must match'))
    ])


class ActivateForm(Form):
    code = StringField(gettext('Activation code'), [DataRequired(), Length(SIZE_UUID)])
