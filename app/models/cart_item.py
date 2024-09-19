from .. import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Reference to the Product model
    quantity = db.Column(db.Integer, nullable=False, default=1)  # Quantity of the product in the cart
    created_by = db.Column(db.Integer, nullable=False)  # The user who added the item
    updated_by = db.Column(db.Integer, nullable=True)  # The user who last updated the item
    deleted_at = db.Column(db.DateTime)
    product = db.relationship('Product')
    user = db.relationship('User') 
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'created_by': self.created_by,
            'updated_by': self.updated_by
        }
