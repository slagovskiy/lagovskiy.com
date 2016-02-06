from flask import Blueprint, render_template, g
from project import app
from .models import MyLink

mod_blog = Blueprint(
    'links',
    __name__,
    url_prefix='/links',
    template_folder='templates'
)


@app.before_request
def before_request():
    g.mylinks = MyLink.query.filter_by(deleted=False)
