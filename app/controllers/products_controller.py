from flask import jsonify, request
from .. import db
from app.models import Product, ProductCategory,ProductMedia,ProductMediaType
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

def register_route(app):
    @app.route('/product/add', methods=['POST'])
    @jwt_required()
    def create_product():
        data = request.get_json()
        files = request.files.getlist('files')
        media_items=[]
        if files:
            for file in files:
                if file.filename == '':
                    continue
                media_item = ProductMedia(
                    media_url='',
                    media_type=''
                )
                media_items.append(media_item)


        #creating product category object
        category = ProductCategory.query.filter_by(id=data['category']).first()
        
        #creating product object
        product = Product(
            name=data['name'],
            description=data['description'],
            marked_price=data['marked_price'],
            discount=data['discount'],
            price=data['price'],
            stock=data['stock'],
            seller_id=get_jwt_identity()['id'],
            category=category,
            media=media_items
        )

        # Add to session and commit
        db.session.add(product)
        db.session.commit()
        return jsonify({"message":"Product inserted successfully"}), 200
    
    # Get products
    @app.route('/products', methods=['GET'])
    def get_products():
        category = request.args.get('category')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        name = request.args.get('name')

        # Start with the base query
        query = Product.query

        # Apply filters dynamically
        if category:
            query = query.join(ProductCategory).filter(ProductCategory.name == category)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        if name:
            query = query.filter(Product.name.ilike(f"%{name}%"))

        # Execute the query and get results
        products = query.all()

        # Convert results to JSON-friendly format
        product_list = [product.to_dict() for product in products]

        return jsonify(product_list), 200
    
    # Get seller products
    @app.route('/products/seller', methods=['GET'])
    @jwt_required()
    def get_products():
        user_id = get_jwt_identity()['id']
        # Start with the base query
        query = Product.query
        query = query.filter(Product.seller_id == user_id)

        # Execute the query and get results
        products = query.all()

        # Convert results to JSON-friendly format
        product_list = [product.to_dict() for product in products]

        return jsonify(product_list), 200


