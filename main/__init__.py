from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from .config import config
# from users import models

app = Flask(__name__)
api = Api(app)
app.config.from_object(config)
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


# Create tables
@app.before_first_request
def create_tables():
    db.create_all()

# @jwt.token_in_blacklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return models.RevokedTokenModel.is_jti_blacklisted(jti)

from users import resources as users_resources
from products import resources as products_resources

api.add_resource(users_resources.UserLogin, '/login')
api.add_resource(users_resources.UserLogoutAccess, '/logout/access')
api.add_resource(users_resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(users_resources.TokenRefresh, '/token/refresh')

# api.add_resource(users_resources.SecretResource, '/secret')

api.add_resource(users_resources.Users, '/users')
api.add_resource(users_resources.UsersDetail, '/users/<string:id>')

api.add_resource(products_resources.Products, '/products')
api.add_resource(products_resources.ProductsDetail, '/products/<string:id>')