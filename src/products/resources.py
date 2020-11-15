from flask_restful import Resource, reqparse
from src.products.models import Product
from flask_jwt_extended import jwt_required

parser = reqparse.RequestParser()
parser.add_argument('id', required=False)
parser.add_argument('name', help='name cannot be blank', required=True)
parser.add_argument('price', help='price cannot be blank', required=True)
parser.add_argument('description', required=False)


class Products(Resource):
    @jwt_required
    def get(self):
        """
        Return all products
        """
        return Product.return_all()

    @jwt_required
    def post(self):
        data = parser.parse_args()
        name = data['name']
        # Checking that user is already exist or not
        if Product.find_by_name(name):
            return {'message': f'Product {name} already exists'}, 400

        # create new user
        item = Product(
            name=name,
            price=data['price'],
            description=data.get('description', ''),
        )

        try:
            # Saving user in DB and Generating Access and Refresh token
            item.save()
            return {
                'payload': {
                    'product': item.to_json(),
                }
            }, 201
        except:
            return {'message': 'Error while saving the product'}, 500

class ProductsDetail(Resource):
    @jwt_required
    def get(self, id):
        """
        Return product
        """
        item = Product.find_by_id(id)
        if item:
            return {
                'payload': {
                    'product': item.to_json()
                }
            }
        return {"messages": "Product not found"}, 404

    @jwt_required
    def put(self, id):
        """
        Edit product data
        """
        parser.replace_argument('name', required=False)
        parser.replace_argument('price', required=False)
        parser.replace_argument('description', required=False)
        data = parser.parse_args()
        item = Product.find_by_id(id)
        if not item:
            return {"messages": "User not found"}, 404

        name = data.get('name', None)
        if name and Product.find_by_name(name):
            return {'message': f'Product {name} already exists'}, 400

        for key, value in data.items():
            if data[key] is not None:
                setattr(item, key, value)

        try:
            item.save()
            return {
                'payload': {
                    'product': item.to_json(),
                }
            }
        except Exception as e:
            return {'message': 'Error while updating the product'}, 500

    @jwt_required
    def delete(self, id):
        """
        Delete user
        """
        item = Product.find_by_id(id)
        if not item:
            return {"messages": "Product not found"}, 404
        try:
            item.delete()
            return {
                "payload": {},
                "messages": "Product deleted"
            }
        except:
            return {'message': 'Something went wrong'}, 500
      