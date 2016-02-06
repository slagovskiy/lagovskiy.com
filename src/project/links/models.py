from datetime import datetime
from uuid import uuid4
from project import db
from .config import SIZE_UUID, SIZE_SLUG, SIZE_NAME


class MyLink(db.Model):
    __tablename__ = 'links_mylink'
    id = db.Column('mylink_id', db.Integer, primary_key=True)
    uuid = db.Column('uuid', db.String(SIZE_UUID), unique=True)
    slug = db.Column('slug', db.String(SIZE_SLUG), unique=True, index=True)
    name = db.Column('name', db.String(SIZE_NAME), default='', index=True)
    link = db.Column('link', db.String(SIZE_NAME), default='', index=True)
    blank = db.Column('blank', db.Boolean, default=True)
    added = db.Column('added', db.DateTime)
    deleted = db.Column('deleted', db.Boolean, default=False)

    def __init__(self, slug, name, link, blank=True):
        self.uuid = str(uuid4())
        self.slug = slug
        self.name = name
        self.link = link
        self.blank = blank
        self.added = datetime.utcnow()

    def __repr__(self):
        return '<MyLink %s [%s]>' % (self.name, self.link)

    @staticmethod
    def exist(slug):
        if MyLink.query.filter_by(slug=slug).first() is None:
            return False
        else:
            return True
