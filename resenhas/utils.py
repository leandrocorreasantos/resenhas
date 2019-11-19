from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


migrate = Migrate()
bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
