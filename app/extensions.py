from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate


# create all the extensions objects

db = SQLAlchemy()

login = LoginManager()

mail = Mail()

migrate = Migrate()