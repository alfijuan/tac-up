from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from .config import configs

api = Api()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app(config_name = "development"):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    # jwt._set_error_handler_callbacks(api)
    migrate.init_app(app, db)

    return app


# Import URL
from src.main import urls