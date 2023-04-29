from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import config

db = SQLAlchemy()
DB_NAME = "database.db"
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    migrate = Migrate(app,db)
    mail.init_app(app)

    #importing the blueprints
    from .auth import auth
    from .task import task

    #adding the blueprints to app
    app.register_blueprint(auth,url_prefix = "/")
    app.register_blueprint(task,url_prefix = "/")

    #errors,like 404
    from .help_functions import errorhandling_init
    errorhandling_init(app)

    #importing the user roles
    from .models import User

    #adding user to login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        db.create_all()

    return app