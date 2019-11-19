import sys
import errno
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from resenhas.app import app, db
from resenhas.models import(  # noqa
    Artigo, ArtigoTag, Tag, Role, User, UserRoles
)


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    roles = [
        {'id': 1, 'name': 'admin'},
        {'id': 2, 'name': 'editor'},
        {'id': 3, 'name': 'writer'},
        {'id': 4, 'name': 'user'},
    ]
    for role in roles:
        new_role = Role(**role)
        try:
            db.session.add(new_role)
            db.session.commit()
        except Exception as e:
            print('Error while write roles. {}'.format(e))


if __name__ == '__main__':
    if not app.debug:
        print("production mode. migration skipped")
        sys.exit(errno.EACCess)
    manager.run()
