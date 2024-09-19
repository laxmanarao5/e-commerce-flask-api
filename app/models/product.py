from .. import db

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    marked_price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)  # Foreign key to the Seller model
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)  # Foreign key to the Category model
    deleted_at = db.Column(db.DateTime)
    media = db.relationship('ProductMedia', back_populates='product')
    orders = db.relationship('Order', backref='product_orders', lazy=True)
    seller = db.relationship('Seller', backref='product_details', lazy=True)


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'marked_price': self.marked_price,
            'discount': self.discount,
            'price': self.price,
            'stock': self.stock,
            'seller_id': self.seller_id,
            'category_id': self.category_id,
            'media': self.media
        }
