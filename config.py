# provide config values for flask app
# this is going to get values from .env file to keep it separate
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / 'instance' / 'salon.db'
class Config:
    SECRET_KEY = "development-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{DATABASE_PATH}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False