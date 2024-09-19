from .. import db

class ProductMediaType(db.Model):
    __tablename__ = 'product_media_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # e.g., 'image', 'video'
    media = db.relationship('ProductMedia', backref='media_type', lazy=True)