from flask import Flask
from resenhas import db, migrate, bootstrap
from .errors.handlers import errors
from .admin.views import admin
# from .blog.views import blog
from .config import Config
from .models import User
from flask_user import UserManager, login_required


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
bootstrap.init_app(app)

user_manager = UserManager(app, db, User)

app.register_blueprint(errors)
app.register_blueprint(admin)


# root site
@app.route('/')
def index():
    return "index"


@app.route('/members')
@login_required
def members():
    return "members only"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
