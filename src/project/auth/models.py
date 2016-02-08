from uuid import uuid1
from datetime import datetime
from sqlalchemy import func
from flask.ext.login import unicode
from project import db, bcrypt
from config import USER_MUST_ACTIVATE_REGISTRATION
from .config import ROLE_USER, SIZE_UUID, SIZE_USERNAME, SIZE_PASSWORD, SIZE_EMAIL


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key=True)
    uuid = db.Column('uuid', db.String(SIZE_UUID), unique=True)
    username = db.Column('username', db.String(SIZE_USERNAME), unique=True, index=True)
    password = db.Column('password', db.String(SIZE_PASSWORD))
    email = db.Column('email', db.String(SIZE_EMAIL), unique=True, index=True)
    role = db.Column('role', db.SmallInteger, default=ROLE_USER)
    active = db.Column('active', db.Boolean, default=True)
    registered = db.Column('registered', db.DateTime)
    last_active = db.Column('last_active', db.DateTime)
    subscribed = db.Column('subscribed', db.Boolean, default=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username, password, email):
        self.uuid = str(uuid1())
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.email = email
        self.active = not USER_MUST_ACTIVATE_REGISTRATION
        self.registered = datetime.utcnow()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def username_exist(username):
        if User.query.filter(func.lower(username) == func.lower(User.username)).first() is None:
            return False
        else:
            return True

    @staticmethod
    def email_exist(email):
        if User.query.filter(func.lower(email) == func.lower(User.email)).first() is None:
            return False
        else:
            return True
