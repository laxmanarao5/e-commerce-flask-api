from flask import jsonify, request
from app.models.product_category import ProductCategory


def register_route(app):
    @app.route('/cat', methods=['GET'])
    def get_all_categories():
        categories = ProductCategory.query.all()
        result = [category.to_dict() for category in categories]
        return jsonify(result), 200



# @app.route('/categories', methods=['POST'])
# def create_category():
#     data = request.get_json()
#     new_category = Category(name=data['name'])
#     db.session.add(new_category)
#     db.session.commit()
#     return jsonify(new_category.to_dict()), 201
