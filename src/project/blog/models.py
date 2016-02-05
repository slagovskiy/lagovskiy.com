from uuid import uuid4
from datetime import datetime
from project import db
from .config import SIZE_NAME, SIZE_UUID


class Tag(db.Model):
    __tablename__ = 'blog_tag'
    id = db.Column('tag_id', db.Integer, primary_key=True)
    uuid = db.Column('uuid', db.String(SIZE_UUID), unique=True)
    slug = db.Column('slug', db.String(SIZE_NAME), unique=True, index=True)
    tagname = db.Column('tagname', db.String(SIZE_NAME), index=True)
    added = db.Column('added', db.DateTime)
    deleted = db.Column('deleted', db.Boolean, default=False)

    def __init__(self, slug, tagname):
        self.uuid = str(uuid4())
        self.slug = slug
        self.tagname = tagname
        self.added = datetime.utcnow()

    def __repr__(self):
        return '<Tag %s [%s]>' % (self.tagname, self.slug)

    @staticmethod
    def exist(slug):
        if Tag.query.filter_by(slug=slug).first() is None:
            return False
        else:
            return True


class Category(db.Model):
    __tablename__ = 'blog_category'
    id = db.Column('category_id', db.Integer, primary_key=True)
    uuid = db.Column('uuid', db.String(SIZE_UUID), unique=True)
    slug = db.Column('slug', db.String(SIZE_NAME), unique=True, index=True)
    categoryname = db.Column('categoryname', db.String(SIZE_NAME), index=True)
    order = db.Column('order', db.SmallInteger(), default=10)
    added = db.Column('added', db.DateTime)
    deleted = db.Column('deleted', db.Boolean, default=False)

    def __init__(self, slug, categoryname):
        self.uuid = str(uuid4())
        self.slug = slug
        self.categoryname = categoryname
        self.added = datetime.utcnow()

    def __repr__(self):
        return '<Category %s [%s]>' % (self.categoryname, self.slug)

    @staticmethod
    def exist(slug):
        if Category.query.filter_by(slug=slug).first() is None:
            return False
        else:
            return True
