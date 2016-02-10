import json
from datetime import datetime
from flask import render_template, g
from flask.ext.login import current_user
from project import app, db


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_active = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/')
@app.route('/index')
def index():
    text = 'Hello, world!\n' \
           '=============\n\n' \
           '[image:124]\n\n' \
           'Test test test test test test test test test test test test test test test test test test test test test test test.\n\n' \
           'Test test test test test test test test test test test test test test test test test test test test test test test.'
    return render_template(
        'index.html',
        text=text
    )


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))
