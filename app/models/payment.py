from .. import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)  # Foreign key to the Order model
    transaction_id = db.Column(db.String(100), nullable=False) 
    amount = db.Column(db.Float, nullable=False)  # Payment amount
    status = db.Column(db.String(50), nullable=False) 
    payment_method = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship('Order', backref=db.backref('payments', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'transaction_id': self.transaction_id,
            'amount': self.amount,
            'status': self.status,
            'payment_method': self.payment_method,
            'created_at': self.created_at
        }
