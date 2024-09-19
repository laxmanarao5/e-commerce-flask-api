from .. import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    deleted_at = db.Column(db.DateTime)
    orders = db.relationship('Order', backref='users',lazy=True)
    carts = db.relationship('CartItem', backref='users', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email':self.email,
            'password':self.password
        }