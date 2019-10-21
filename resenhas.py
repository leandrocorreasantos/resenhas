from flask import Flask, send_from_directory
from . import db, migrate, bootstrap
from .config import MediaConfig
from .errors.handlers import errors
from .admin.views import admin
from .blog.views import blog
# from .config import Config
from .models import User
from flask_user import UserManager


def create_app(app_name='app', config_obj='resenhas.config.Config'):
    app = Flask(app_name)
    app.config.from_object(config_obj)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    app.register_blueprint(admin)
    app.register_blueprint(blog)
    app.register_blueprint(errors)
    user_manager = UserManager(app, db, User)  # noqa
    return app


app = create_app(__name__)


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(MediaConfig.MEDIA_ROOT, filename)


# # root site
# @app.route('/')
# def index():
#     return "index"
#
#
# @app.route('/members')
# @login_required
# def members():
#     return "members only"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True, threaded=True)
