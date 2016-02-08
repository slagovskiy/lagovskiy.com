from flask import Blueprint, render_template, g, redirect, url_for
from project import app
from sqlalchemy import func
from .models import Tag, Category, Post
from .config import POST_STATUS_PUBLISHED

mod_blog = Blueprint(
    'blog',
    __name__,
    url_prefix='/blog',
    template_folder='templates'
)


@app.before_request
def before_request():
    g.tags = Tag.query.filter_by(deleted=False)
    g.categories = Category.query.filter_by(deleted=False).order_by('order')


@mod_blog.route('/', methods=['GET'])
def index():
    posts = Post.query.filter_by(status=POST_STATUS_PUBLISHED)
    return render_template(
        'posts.html',
        posts=posts
    )


@mod_blog.route('/tag/<slug>', methods=['GET'])
def posts_by_tag(slug=None):
    t = Tag.query.filter(func.lower(slug) == func.lower(Tag.slug)).first()
    posts = None
    if t:
        posts = t.posts.filter_by(status=POST_STATUS_PUBLISHED).order_by('-published').all()
        return render_template(
            'posts.html',
            posts=posts,
            active_tag=t
        )
    else:
        return redirect(url_for('blog.index'))


@mod_blog.route('/category/<slug>', methods=['GET'])
def posts_by_category(slug=None):
    c = Category.query.filter(func.lower(slug) == func.lower(Category.slug)).first()
    posts = None
    if c:
        posts = c.posts.filter_by(status=POST_STATUS_PUBLISHED).order_by('-published').all()
        return render_template(
            'posts.html',
            posts=posts,
            active_category=c
        )
    else:
        return redirect(url_for('blog.index'))
