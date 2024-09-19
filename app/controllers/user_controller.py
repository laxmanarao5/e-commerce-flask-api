from flask import jsonify, request, make_response
from .. import db
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt

def register_route(app):
    # seller registration
    @app.route('/user/register', methods=['POST'])
    def user_registration():
        data = request.get_json() 
        bcrypt = Bcrypt(app)
        # Check if the seller already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({"message": "User with this email already exists"}), 400
        new_user = User(name=data['name'], email=data['email'], password= bcrypt.generate_password_hash(data['password']).decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()
        return jsonify(
            {
                "message":"User registration successfull"
            }
        )
    # seller Login
    @app.route('/user/login', methods=['POST'])
    def user_login():
        # Bcrypt Initialization
        bcrypt = Bcrypt(app)
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            user_dict =user.to_dict()
            del user_dict['password']
            access_token = create_access_token(identity=user_dict)
            return jsonify({'message': 'Login Successful', 'access_token': access_token, "user":user_dict})
        return make_response(jsonify({"error": "Unauthorized access"}), 401)



