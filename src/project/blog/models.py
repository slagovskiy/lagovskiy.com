from uuid import uuid4
from datetime import datetime
from project import db
from .config import SIZE_NAME, SIZE_UUID, SIZE_TITLE, SIZE_META
from .config import POST_STATUS_DRAFT, POST_TEMPLATE_TEXT


tags = db.Table(
    'blog_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('blog_tag.tag_id')),
    db.Column('post_id', db.Integer, db.ForeignKey('blog_post.post_id'))
)


categories = db.Table(
    'blog_categories',
    db.Column('category_id', db.Integer, db.ForeignKey('blog_category.category_id')),
    db.Column('post_id', db.Integer, db.ForeignKey('blog_post.post_id'))
)


class Tag(db.Model):
    __tablename__ = 'blog_tag'
    id = db.Column('tag_id', db.Integer, primary_key=True)
    uuid = db.Column('uuid', db.String(SIZE_UUID), unique=True)
    slug = db.Column('slug', db.String(SIZE_NAME), unique=True, index=True)
    name = db.Column('name', db.String(SIZE_NAME), index=True)
    added = db.Column('added', db.DateTime)
    deleted = db.Column('deleted', db.Boolean, default=False)

    def __init__(self, slug, name):
        self.uuid = str(uuid4())
        self.slug = slug
        self.name = name
        self.added = datetime.utcnow()

    def __repr__(self):
        return '<Tag %s [%s]>' % (self.name, self.slug)

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
    name = db.Column('name', db.String(SIZE_NAME), index=True)
    order = db.Column('order', db.SmallInteger(), default=10)
    added = db.Column('added', db.DateTime)
    deleted = db.Column('deleted', db.Boolean, default=False)

    def __init__(self, slug, name):
        self.uuid = str(uuid4())
        self.slug = slug
        self.name = name
        self.added = datetime.utcnow()

    def __repr__(self):
        return '<Category %s [%s]>' % (self.name, self.slug)

    @staticmethod
    def exist(slug):
        if Category.query.filter_by(slug=slug).first() is None:
            return False
        else:
            return True


class Post(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column('post_id', db.Integer, primary_key=True)
    uuid = db.Column('uuid', db.String(SIZE_UUID), unique=True)
    slug = db.Column('slug', db.String(SIZE_TITLE), unique=True, index=True)
    description = db.Column('description', db.String(SIZE_META), default='')
    keywords = db.Column('keywords', db.String(SIZE_META), default='')
    status = db.Column('status', db.SmallInteger, default=POST_STATUS_DRAFT)
    added = db.Column('added', db.DateTime)
    published = db.Column('published', db.DateTime)
    sticked = db.Column('sticked', db.Boolean, default=False)
    ping = db.Column('ping', db.Boolean, default=False)
    comments_enabled = db.Column('comments_enabled', db.Boolean, default=True)
    comments_moderated = db.Column('comments_moderated', db.Boolean, default=False)
    template = db.Column('template', db.SmallInteger, default=POST_TEMPLATE_TEXT)
    title = db.Column('title', db.String(SIZE_TITLE), index=True, default='')
    teaser = db.Column('teaser', db.Text, default='')
    content = db.Column('content', db.Text, default='')
    prev = db.Column('prev', db.Text, default='')
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'))
    categories = db.relationship('Category', secondary=categories, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self):
        self.uuid = str(uuid4())
        self.added = datetime.utcnow()

    def __repr__(self):
        return '<Post: %s>' % self.title

    @staticmethod
    def exist(slug):
        if Post.query.filter_by(slug=slug).first() is None:
            return False
        else:
            return True
