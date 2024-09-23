from .. import db

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    cancelled_at = db.Column(db.DateTime, nullable=True)
    created_at =  db.Column(db.DateTime)
    status = db.Column(db.String(100), nullable=False)
    deleted_at = db.Column(db.DateTime)
    user = db.relationship('User') 
    product = db.relationship('Product')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'total_price': self.total_price,
            'cancelled_at': self.cancelled_at
        }