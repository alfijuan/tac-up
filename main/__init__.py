from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from .config import config

app = Flask(__name__)
api = Api(app)
app.config.from_object(config)
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


# Import URL
from main import urls