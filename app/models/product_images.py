from .. import db

class ProductImages(db.Model):
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False) 
    image = db.Column(db.String(255), nullable=False)

    product = db.relationship('Product', back_populates='images')
    def to_dict(self):
        return {
            'id': self.id,
            'image':self.image
        }