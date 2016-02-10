from uuid import uuid4
from datetime import datetime
from project import db
from .config import SIZE_UUID, SIZE_FILENAME, SIZE_TYPE


class MediaFolder(db.Model):
    __tablename__ = 'media_folder'
    id = db.Column('folder_id', db.Integer, primary_key=True)
    uuid = db.Column('uuid', db.String(SIZE_UUID), unique=True)
    name = db.Column('name', db.String(SIZE_FILENAME), default='')
    added = db.Column('added', db.DateTime)
    rename = db.Column('rename', db.Boolean, default=True)
    deleted = db.Column('deleted', db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    files = db.relationship('MediaFile', backref='folder', lazy='dynamic')

    def __init__(self, name):
        self.uuid = str(uuid4())
        self.name = name
        self.added = datetime.utcnow()

    def __repr__(self):
        return '<Mediafolder %s>' % self.name


class MediaFile(db.Model):
    __tablename__ = 'media_file'
    id = db.Column('file_id', db.Integer, primary_key=True)
    uuid = db.Column('uuid', db.String(SIZE_UUID), unique=True)
    name = db.Column('name', db.String(SIZE_FILENAME), default='')
    ext = db.Column('ext', db.String(SIZE_TYPE), default='')
    added = db.Column('added', db.DateTime)
    deleted = db.Column('deleted', db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    folder_id = db.Column(db.Integer, db.ForeignKey('media_folder.folder_id'))

    def __init__(self, uuid, folder, name, ext):
        self.uuid = uuid
        self.folder = folder
        self.name = name
        self.ext = ext
        self.added = datetime.utcnow()

    def __repr__(self):
        return '<Mediafile %s>' % self.name
