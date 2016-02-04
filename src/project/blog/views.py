from flask import Blueprint, render_template, g
from project import app
from .models import Tag

mod_blog = Blueprint(
    'blog',
    __name__,
    url_prefix='/blog',
    template_folder='templates'
)


@app.before_request
def before_request():
    g.tags = Tag.query.filter_by(deleted=False)


@mod_blog.route('/', methods=['GET'])
def index():
    return render_template('posts.html')


@mod_blog.route('/tag/<slug>', methods=['GET'])
def posts_by_tag(slug=None):
    return render_template('index.html')
