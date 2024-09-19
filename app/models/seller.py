from .. import db
from datetime import datetime

class Seller(db.Model):
    __tablename__ = 'sellers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)
    products = db.relationship('Product', backref='seller_details', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'emaiil':self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'password':self.password
        }
