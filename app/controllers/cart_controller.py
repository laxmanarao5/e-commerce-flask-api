from flask import jsonify, request
from .. import db
from app.models import CartItem
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
def register_route(app):
    # add item to cart
    @app.route('/cart/add', methods=['POST'])
    @jwt_required()
    def create_cart_product():
        data = request.get_json()
        print(data)
        user_id = get_jwt_identity()['id']
        cart_item = CartItem.query.filter(
            CartItem.user_id == user_id,
            CartItem.product_id == data['product_id'],
            CartItem.deleted_at.is_(None)  
        ).first()
        if cart_item:
            cart_item.quantity = cart_item.quantity + 1
            cart_item.updated_at = datetime.utcnow()  # Assuming you have an updated_at field
        else:
            cart_item = CartItem(
                user_id = user_id,
                product_id = data['product_id'],
                quantity = data['quantity'],
                created_by = user_id,
                updated_by = user_id
            )
            # Add to session and commit
            db.session.add(cart_item)
        db.session.commit()
        return jsonify({"message":"Product added to cart successfully"}), 200
    
    # Get cart items
    @app.route('/cart/items', methods=['GET'])
    @jwt_required()
    def get_cart_items():
        user_id = get_jwt_identity()['id']
        cart_items = CartItem.query.filter_by(
            user_id = user_id, deleted_at = None
        ).all()

        # Convert results to JSON-friendly format
        cart_items_dict = [item.to_dict() for item in cart_items]

        return jsonify({
            "message":"all products in cart", "data": cart_items_dict
        }), 200
    
    # Remove cart items
    @app.route('/cart/remove', methods=['PUT'])
    @jwt_required()
    def remove_cart_items():
        data = request.get_json()
        user_id = get_jwt_identity()['id']
        CartItem.query.filter(
            CartItem.user_id == user_id,
            CartItem.id == data['cart_item_id'],
            CartItem.deleted_at.is_(None)  
        ).update(
            {CartItem.deleted_at: datetime.utcnow()},
            synchronize_session='fetch' 
        )
        # Commit the changes to the database
        db.session.commit()
        return jsonify({
            "message":"Product removed from cart"
        }), 200
    
    # Update cart item quantity
    @app.route('/cart/quantity', methods=['PUT'])
    @jwt_required()
    def change_qnt():
        data = request.get_json()
        user_id = get_jwt_identity()['id']
        CartItem.query.filter(
            CartItem.user_id == user_id,
            CartItem.id == data['cart_item_id'],
            CartItem.deleted_at.is_(None)  
        ).update(
            {CartItem.quantity: data['quantity']},
            synchronize_session='fetch' 
        )
        # Commit the changes to the database
        db.session.commit()
        return jsonify({
            "message":"Quatity Updated"
        }), 200
    



