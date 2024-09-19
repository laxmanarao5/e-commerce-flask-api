from .. import db

class ProductMedia(db.Model):
    __tablename__ = 'product_media'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False) 
    media_type_id = db.Column(db.Integer, db.ForeignKey('product_media_type.id'), nullable=False)  # Reference to ProductMediaType 
    media_url = db.Column(db.String(255), nullable=False)

    product = db.relationship('Product', back_populates='media')
