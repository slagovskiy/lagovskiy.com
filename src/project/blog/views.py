from flask import Blueprint, render_template


mod_blog = Blueprint(
    'blog',
    __name__,
    url_prefix='/blog',
    template_folder='templates'
)


@mod_blog.route('/', methods=['GET'])
def index():
    return render_template('posts.html')
