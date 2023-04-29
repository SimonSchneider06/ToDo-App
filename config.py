import os 
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir + ".env")
load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "7lK8t(?kitioeo(w9tl;)"
    MAIL_SERVER = os.environ.get("MAIL_SERVER","smtp.1und1.de")
    MAIL_PORT = os.environ.get("MAIL_PORT","587")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS","true").lower() in ["true","on","1"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_PREFIX = "ToDo-App"
    MAIL_SENDER = ""
    FLASK_APP = os.environ.get("FLASK_APP")
    # ADMIN = os.environ.get("ADMIN")
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or f"sqlite:///database.db"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite://"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///productionDatabase.db"

config = {
    "development":DevelopmentConfig,
    "testing":TestingConfig,
    "production":ProductionConfig,

    "default":DevelopmentConfig
}