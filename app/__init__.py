# when init is run, it creates the flask app with the objects created in config
# and extensions along with the variables defined in each respective class

from flask import Flask

from config import Config
from app.extensions import db, login, mail, migrate
from app.main import main
from app.models import User
from app.auth import auth


def create_app():
    """application "factory" - create a flask app"""

    app = Flask(__name__) # create the app

    app.config.from_object(Config) # use  the configuration object define in config class

    # each extension object we've already created is being attached to the app we made just above (atm line 11)
    register_extensions(app)
    register_blueprints(app)

    return app

def register_extensions(app):
    """initialize flask extensions"""
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(main)
    app.register_blueprint(auth)

@login.user_loader
def load_user(user_id):
    """Load a user from the database by their ID."""
    return db.session.get(User, int(user_id))