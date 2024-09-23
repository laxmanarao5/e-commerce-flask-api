from flask import jsonify, request
from .. import db
from app.models import Order,CartItem
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
def register_route(app):
    # add item to cart
    @app.route('/order', methods=['POST'])
    @jwt_required()
    def create_order():
        user_id = get_jwt_identity()['id']
        cart_items = CartItem.query.filter(
            CartItem.user_id == user_id,
            CartItem.deleted_at.is_(None)
        ).all()
 
        if not cart_items:
            return jsonify({"message":"Items not found in cart"}), 200
        for cart_item in cart_items:
            order = Order(
                user_id=user_id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                status = 'Shipped',
                created_at= datetime.utcnow(),
                total_price=cart_item.product.price * cart_item.quantity,
            )
            db.session.add(order)
            # Deleting item in cart
            cart_item.deleted_at = datetime.utcnow()
 
        # Commit all changes to the database
        db.session.commit()
        return jsonify({"message":"Order placed successfully"}), 200
       
    
    # cancel Item
    @app.route('/order/cancel', methods=['PUT'])
    @jwt_required()
    def cancel_order():
        user_id = get_jwt_identity()['id']
        data = request.get_json()
        Order.query.filter(
            Order.user_id == user_id,
            Order.id == data['order_id'],
            Order.deleted_at.is_(None)  
        ).update(
            {Order.cancelled_at: datetime.utcnow()},
            synchronize_session='fetch' 
        )
        # Commit all changes to the database
        db.session.commit()
        return jsonify({"message":"Order cancelled successfully"}), 200
       

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


