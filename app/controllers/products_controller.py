from flask import jsonify, request
from .. import db
from app.models import Product, ProductCategory,ProductImages
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
import os
import boto3
from dotenv import load_dotenv
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID1')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY1')
REGION_NAME = os.getenv('REGION_NAME1')
S3_BUCKET = os.getenv('S3_BUCKET')
# Initialize S3 client
s3_client = boto3.client(
    's3',
    region_name=REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def register_route(app):
    @app.route('/product/add', methods=['POST'])
    @jwt_required()
    def create_product():
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        description = request.form['description']
        stock = request.form['stock']
        marked_price = request.form['marked_price']
        discount = request.form['discount']
        file = request.files['image']
        if file : 
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{name}_{timestamp}.{file.filename.rsplit('.', 1)[1].lower()}"
            s3_key = f"products/{filename}"
            s3_client.upload_fileobj(
            file,
            S3_BUCKET,
            s3_key
        )
            # s3_client.upload_fileobj(file, S3_BUCKET, s3_key, ExtraArgs={"ACL": "public-read"})
            image_url = f"https://{S3_BUCKET}.s3.{REGION_NAME}.amazonaws.com/{s3_key}"
            product_image = ProductImages(
                image=image_url
            )

        #creating product category object
        category = ProductCategory.query.filter_by(id=category).first()
        
        #creating product object
        product = Product(
            name=name,
            description=description,
            marked_price=marked_price,
            discount=discount,
            price=price,
            stock=stock,
            seller_id=get_jwt_identity()['id'],
            category=category,
            images = [product_image]
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
            query = query.join(ProductCategory).filter(ProductCategory.id == category)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        if name:
            query = query.filter(Product.name.ilike(f"%{name}%"))

        # Execute the query and get results
        products = query.all()

        product_list = [product.to_dict() for product in products]

        # Print the final list for debugging (optional)
        print(product_list)
        return jsonify(product_list), 200
    
    # Get seller products
    @app.route('/products/seller', methods=['GET'])
    @jwt_required()
    def get_seller_products():
        user_id = get_jwt_identity()['id']

        # Execute the query and get results
        products = Product.query.filter(Product.seller_id == user_id, Product.deleted_at.is_(None))

        # Convert results to JSON-friendly format
        product_list = [product.to_dict() for product in products]

        return jsonify(product_list), 200

    # Delete product
    @app.route('/product/remove', methods=['PUT'])
    @jwt_required()
    def delete_products():
        user_id = get_jwt_identity()['id']
        data = request.get_json()
        Product.query.filter(
            Product.seller_id == user_id,
            Product.id == data['product_id'],
            Product.deleted_at.is_(None)  
        ).update(
            {Product.deleted_at: datetime.utcnow()},
            synchronize_session='fetch' 
        )
        # Commit all changes to the database
        db.session.commit()
        return jsonify({"message":"Product deleted successfully"}), 200

