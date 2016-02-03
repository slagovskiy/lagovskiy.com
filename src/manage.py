from project import app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from config import SQLALCHEMY_MIGRATE_REPO

migrate = Migrate(
    app=app,
    db=db,
    directory=SQLALCHEMY_MIGRATE_REPO
)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
