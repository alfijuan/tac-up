from main import db


class Product(db.Model):
    """
    Product Model Class
    """
    __tablename__ = 'products'
    __bind_key__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(400), nullable=True)
    price = db.Column(db.DECIMAL(10,2), nullable=False)

    """
    Save product details in database
    """
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    """
    Delete product
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
            'name': self.name,
            'price': str(round(self.price, 2)),
            'description': self.description
        }

    """
    Find user by name
    """
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    """
    Find user by id
    """
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    """
    Return all products
    """
    @classmethod
    def return_all(cls):
        return {'products': [prod.to_json() for prod in Product.query.all()]}

    
    """
    Delete all products
    """
    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': f'{num_rows_deleted} row(s) deleted'}
        except:
            return {'message': 'Something went wrong'}, 500