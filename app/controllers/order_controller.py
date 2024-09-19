from flask import jsonify, request
from .. import db
from app.models import Order
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
def register_route(app):
    # add item to cart
    @app.route('/order', methods=['POST'])
    @jwt_required()
    def create_order():
        data = request.get_json()
        user_id = get_jwt_identity()['id']
        
    #     cart_item = CartItem(
    #         user_id = user_id,
    #         product_id = data['product_id'],
    #         quantity = data['quantity'],
    #         created_by = user_id,
    #         updated_by = user_id
    #     )

    #     # Add to session and commit
    #     db.session.add(cart_item)
    #     db.session.commit()
    #     return jsonify({"message":"Product added to cart successfully"}), 200
    
    # Get orders
    @app.route('/orders', methods=['GET'])
    @jwt_required()
    def get_orders():
        user_id = get_jwt_identity()['id']
        orders = Order.query.filter_by(
            user_id = user_id, deleted_at = None
        ).all()

        # Convert results to JSON-friendly format
        orders_dict = [item.to_dict() for item in orders]

        return jsonify({
            "message":"all orders", "data": orders_dict
        }), 200
    
    # # Get cart items
    # @app.route('/cart/remove', methods=['PUT'])
    # @jwt_required()
    # def remove_cart_items():
    #     data = request.get_json()
    #     user_id = get_jwt_identity()['id']
    #     CartItem.query.filter(
    #         CartItem.user_id == user_id,
    #         CartItem.id == data['cart_item_id'],
    #         CartItem.deleted_at.is_(None)  
    #     ).update(
    #         {CartItem.deleted_at: datetime.utcnow()},
    #         synchronize_session='fetch' 
    #     )
    #     # Commit the changes to the database
    #     db.session.commit()
    #     return jsonify({
    #         "message":"Product removed from cart"
    #     }), 200



