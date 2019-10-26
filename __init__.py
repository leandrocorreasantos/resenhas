from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
mail = Mail()
