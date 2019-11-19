#!venv/bin/python3
# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_user import UserManager
from resenhas.config import Config
from resenhas.utils import db, bootstrap, mail
from resenhas.models import User
from views.main import main_bp
from views.blog import blog
from views.admin import admin

dotenv_path = os.path.join(os.getcwd(), '.env')
if os.path.isfile(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)


def create_app(name_app):
    app = Flask(name_app)
    app.config.from_object(Config)
    db.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(blog)
    app.register_blueprint(admin)
    return app


app = create_app(__name__)

user_manager = UserManager(app, db, User)  # noqa

# @TODO inspiração https://github.com/koon-kai/kiblog
# http_server = WSGIServer(('', 80), app)
# http_server.serve_forever()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
