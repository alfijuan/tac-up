from main import db
from passlib.hash import pbkdf2_sha256 as sha256
from sales.models import Sale

class User(db.Model):
    """
    User Model Class
    """
    __tablename__ = 'user'
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)

    """
    Save user details in database
    """
    def save(self):
        db.session.add(self)
        db.session.commit()

    """
    Delete user
    """
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """
    Generate json data
    """
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

    """
    Find user by username
    """
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    """
    Find user by id
    """
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    """
    Return all the user data
    """
    @classmethod
    def return_all(cls):
        return {'users': [user.to_json() for user in User.query.all()]}

    """
    Delete user data
    """
    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': f'{num_rows_deleted} row(s) deleted'}
        except:
            return {'message': 'Something went wrong'}, 500

    """
    Generate hash from password
    """
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    """
    Verify hash and password
    """
    @staticmethod
    def verify_hash(password, hash_):
        return sha256.verify(password, hash_)


class RevokedTokenModel(db.Model):
    """
    Revoked Token Model Class
    """
    __tablename__ = 'revoked_tokens'
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    """
    Save Token in DB
    """
    def add(self):
        db.session.add(self)
        db.session.commit()

    """
    Checking that token is blacklisted
    """
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)