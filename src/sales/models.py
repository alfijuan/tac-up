from src.main import db
from datetime import datetime

class Sale(db.Model):
    """
    Sale Model Class
    """
    __tablename__ = 'sale'
    __bind_key__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(), index=True, default=datetime.now)
    commission_paid = db.Column(db.Boolean, default=False, nullable=False)

    """
    Save sale details in database
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
            'user_id': self.user_id,
            'product_id': self.product_id,
            'date': self.date.strftime('%Y-%m-%d'),
            'commission_paid': self.commission_paid
        }

    """
    Find sale by id
    """
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    """
    Return all the sales data
    """
    @classmethod
    def return_all(cls):
        return {'sales': [sale.to_json() for sale in Sale.query.all()]}

    """
    Delete sales data
    """
    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': f'{num_rows_deleted} row(s) deleted'}
        except:
            return {'message': 'Something went wrong'}, 500