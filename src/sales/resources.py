from flask_restful import Resource, reqparse
from src.sales.models import Sale
from src.products.models import Product
from src.users.models import User
from decimal import Decimal
from flask_jwt_extended import jwt_required
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument('id', required=False)
parser.add_argument('user_id', help='user_id cannot be blank', required=True)
parser.add_argument('product_id', help='product_id cannot be blank', required=True)
parser.add_argument('date', required=False)
parser.add_argument('commission_paid', required=False)

class Sales(Resource):
    @jwt_required
    def get(self):
        """
        Return all sales
        """
        return Sale.return_all()

    @jwt_required
    def post(self):

        parser.replace_argument('user_id', help='user_id cannot be blank', required=True)
        parser.replace_argument('product_id', help='product_id cannot be blank', required=True)
        data = parser.parse_args()

        user_id = data.get('user_id')
        if not User.find_by_id(user_id):
            return {'message': f'User {user_id} doesn\'t exist'}, 404

        product_id = data.get('product_id')
        if not Product.find_by_id(product_id):
            return {'message': f'Product {product_id} doesn\'t exist'}, 404

        # create new user
        item = Sale(
            user_id=data.get('user_id'),
            product_id=data.get('product_id')
        )

        if data.get('date'):
            item.date = datetime.strptime(data.get('date'), '%Y-%m-%d')

        if data.get('commission_paid'):
            item.commission_paid = data.get('commission_paid')

        try:
            # Saving user in DB and Generating Access and Refresh token
            item.save()
            return {
                'payload': {
                    'sale': item.to_json(),
                }
            }, 201
        except Exception as e:
            print(e)
            return {'message': 'Error while saving the sale'}, 500

class SalesDetail(Resource):
    @jwt_required
    def get(self, id):
        """
        Return sale
        """
        item = Sale.find_by_id(id)
        if item:
            return {
                'payload': {
                    'sale': item.to_json()
                }
            }
        return {"messages": "Sale not found"}, 404

    @jwt_required
    def put(self, id):
        """
        Edit sale data
        """
        parser.replace_argument('user_id', help='user_id cannot be blank', required=False)
        parser.replace_argument('product_id', help='product_id cannot be blank', required=False)
        data = parser.parse_args()

        user_id = data.get('user_id')
        if user_id:
            if not User.find_by_id(user_id):
                return {'message': f'User {user_id} doesn\'t exist'}, 400

        product_id = data.get('product_id')
        if product_id:
            if not Product.find_by_id(product_id):
                return {'message': f'Product {product_id} doesn\'t exist'}, 400
        
        item = Sale.find_by_id(id)

        if not item:
            return {"messages": "Sale not found"}, 404

        for key, value in data.items():
            if data[key] is not None:
                setattr(item, key, value)

        try:
            item.save()
            return {
                'payload': {
                    'sale': item.to_json(),
                }
            }
        except Exception as e:
            return {'message': 'Error while updating the sale'}, 500
    
    @jwt_required
    def delete(self, id):
        """
        Delete user
        """
        item = Sale.find_by_id(id)
        if not item:
            return {"messages": "Sale not found"}, 404
        try:
            item.delete()
            return {
                "payload": {},
                "messages": "Sale deleted"
            }
        except:
            return {'message': 'Error while deleting the sale'}, 500

class SalesCommissions(Resource):
    @jwt_required
    def get(self, user_id):
        """
        Calculates the amount of commissions that has to be payed
        to the user in a determinate time
        """
        if not User.find_by_id(user_id):
            return {'message': f'User {user_id} doesn\'t exist'}, 404

        try:
            sales = Sale.query.filter_by(user_id=user_id, commission_paid=False)
            products_id = [x.product_id for x in sales]
            products = Product.query.filter(Product.id.in_(products_id)).all()

            total = sum(x.price for x in products)

            commissions = 0
            if total >= 100000 or len(products) >= 7:
                commissions = total * Decimal(0.07)
            else:
                commissions = total * Decimal(0.04)

            return {
                'sales': [x.to_json() for x in sales],
                'total': str(total),
                'commissions': str(round(commissions, 3))
            }
        except:
            return {'message': 'Error while calculating commissions'}, 500

    @jwt_required
    def post(self, user_id):
        """
        Calculates the amount of commissions that has to be payed
        to the user in a determinate time
        """
        if not User.find_by_id(user_id):
            return {'message': f'User {user_id} doesn\'t exist'}, 404

        try:
            sales = Sale.query.filter_by(user_id=user_id, commission_paid=False)
            for s in sales:
                s.commission_paid = True
                s.save()

            return {
                'payload': {},
                'message': f'Commissions payed for user {user_id}'
            }
        except:
            return {'message': 'Error while calculating commissions'}, 500