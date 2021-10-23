from os import getenv, urandom


class Config:
    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    # Flask
    ENV = "DEVELOPMENT"
    DEBUG = True
    SECRET_KEY = "12345678"
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"


class Production(Config):
    # Flask
    ENV = "PRODUCTION"
    SECRET_KEY = urandom(32)
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")


configs = {
    "development": Development,
    "production": Production,
}