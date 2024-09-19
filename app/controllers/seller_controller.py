from flask import jsonify, request, make_response
from .. import db
from app.models import Seller
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt

def register_route(app):
    # seller registration
    @app.route('/seller/register', methods=['POST'])
    def seller_registration():
        data = request.get_json() 
        bcrypt = Bcrypt(app)
        # Check if the seller already exists
        existing_seller = Seller.query.filter_by(email=data['email']).first()
        if existing_seller:
            return jsonify({"message": "Seller with this email already exists"}), 400
        new_seller = Seller(name=data['name'], email=data['email'], password= bcrypt.generate_password_hash(data['password']).decode('utf-8'))
        db.session.add(new_seller)
        db.session.commit()
        return jsonify(
            {
                "message":"Seller registration successfull"
            }
        )
    # seller Login
    @app.route('/seller/login', methods=['POST'])
    def seller_login():
        # Bcrypt Initialization
        bcrypt = Bcrypt(app)
        data = request.get_json()
        seller = Seller.query.filter_by(email=data['email']).first()
        print(seller)
        if seller and bcrypt.check_password_hash(seller.password, data['password']):
            seller_dict =seller.to_dict()
            del seller_dict['password']
            access_token = create_access_token(identity=seller_dict)
            return jsonify({'message': 'Login Successful', 'access_token': access_token, "seller":seller_dict})
        return make_response(jsonify({"error": "Unauthorized access"}), 401)



