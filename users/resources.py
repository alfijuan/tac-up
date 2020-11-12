from flask_restful import Resource, reqparse, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
import pdb

from users.models import User, RevokedTokenModel

parser = reqparse.RequestParser()
parser.add_argument('username', required=True, help='username cannot be blank')
parser.add_argument('password', required=True, help='password cannot be blank')
parser.add_argument('id', required=False)
parser.add_argument('first_name', required=False)
parser.add_argument('last_name', required=False)


class UserLogin(Resource):
    """
    User Login Api
    """
    def post(self):
        parser.replace_argument('password', required=True, help='password cannot be blank')
        data = parser.parse_args()
        username = data['username']

        # Searching user by username
        current_user = User.find_by_username(username)

        # user does not exists
        if not current_user:
            return {'message': f'User {username} doesn\'t exist'}, 400

        # user exists, comparing password and hash
        if User.verify_hash(data['password'], current_user.password):
            # generating access token and refresh token
            access_token = create_access_token(identity=username)        
            refresh_token = create_refresh_token(identity=username)
            return {
                'payload': {
                    'user': current_user.to_json(),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccess(Resource):
    """
    User Logout Api 
    """
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            # Revoking access token
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {
                'message': 'Access token has been revoked',
                'payload': {}
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    """
    User Logout Refresh Api 
    """
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            pdb.set_trace()
            return {
                'message': 'Refresh token has been revoked',
                'payload': {}
            }
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    """
    Token Refresh Api
    """
    @jwt_refresh_token_required
    def post(self): 
        # Generating new access token
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class Users(Resource):
    def get(self):
        """
        Return all users
        """
        return User.return_all()

    def post(self):
        parser.replace_argument('password', required=True, help='password cannot be blank')
        data = parser.parse_args()
        username = data['username']
        # Checking that user is already exist or not
        if User.find_by_username(username):
            return {'message': f'User {username} already exists'}, 400

        # create new user
        new_user = User(
            username=username,
            password=User.generate_hash(data['password']),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )

        try:
            # Saving user in DB and Generating Access and Refresh token
            new_user.save()
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                'payload': {
                    'user': new_user.to_json(),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }, 201
        except:
            return {'message': 'Something went wrong'}, 500

    def delete(self):
        """
        Delete all users
        """
        return User.delete_all()


class UsersDetail(Resource):
    def get(self, id):
        """
        Return user
        """
        user = User.find_by_id(id)
        if user:
            return {
                'payload': {
                    'user': user.to_json()
                }
            }
        return {"messages": "User not found"}, 404

    def put(self, id):
        """
        Edit user data
        """
        parser.replace_argument('password', required=False)
        parser.replace_argument('username', required=False)
        data = parser.parse_args()
        user = User.find_by_id(id)
        if not user:
            return {"messages": "User not found"}, 404

        username = data.get('username', None)
        if username and User.find_by_username(username):
            return {'message': f'User {username} already exists'}, 400

        for key, value in data.items():
            if data[key] is not None:
                setattr(user, key, value)
        try:
            # Saving user in DB and Generating Access and Refresh token
            user.save()
            return {
                'payload': {
                    'user': user.to_json(),
                }
            }
        except:
            return {'message': 'Something went wrong'}, 500

    def delete(self, id):
        """
        Delete user
        """
        user = User.find_by_id(id)
        if not user:
            return {"messages": "User not found"}, 404
        try:
            user.delete()
            return {
                "payload": {},
                "messages": "User deleted"
            }
        except:
            return {'message': 'Something went wrong'}, 500


class SecretResource(Resource):
    """
    Example of required jwt resource
    """
    @jwt_required
    def get(self):
        return {'answer': 'You are accessing super secret blueprint'}