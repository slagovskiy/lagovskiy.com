import os
import unittest
from config import basedir
from project import app, db
from project.auth.models import User
from project.blog.models import Tag, Category
from coverage import coverage


cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_users(self):
        u = User(username='sergey', email='sergey@lagovskiy.com', password='123')
        db.session.add(u)
        db.session.commit()
        u = User.query.filter_by(username='sergey').first()
        assert u.username == 'sergey'
        assert u.is_authenticated is True
        assert u.is_active is True
        u.active = False
        assert u.is_active is False
        assert u.is_anonymous is False
        id = u.get_id()
        assert u.id == id

    def test_blog_tag(self):
        t = Tag(slug='test', tagname='Test')
        db.session.add(t)
        db.session.commit()
        t = Tag.query.filter_by(slug='test').first()
        assert t.slug == 'test'


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    # print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    # cov.html_report(directory='tmp/coverage')
    cov.erase()
