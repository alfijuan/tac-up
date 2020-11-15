from src.main import api
from src.users import resources as users_resources
from src.products import resources as products_resources
from src.sales import resources as sales_resources

api.add_resource(users_resources.UserLogin, '/login')
api.add_resource(users_resources.UserLogoutAccess, '/logout/access')
api.add_resource(users_resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(users_resources.TokenRefresh, '/token/refresh')

# api.add_resource(users_resources.SecretResource, '/secret')

api.add_resource(users_resources.Users, '/users')
api.add_resource(users_resources.UsersDetail, '/users/<string:id>')

api.add_resource(products_resources.Products, '/products')
api.add_resource(products_resources.ProductsDetail, '/products/<string:id>')

api.add_resource(sales_resources.Sales, '/sales')
api.add_resource(sales_resources.SalesDetail, '/sales/<string:id>')

api.add_resource(sales_resources.SalesCommissions, '/commissions/<string:user_id>')