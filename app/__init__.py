import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .config import Config
from flask_cors import CORS
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Allow CORS for specific origins (localhost and CloudFront)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})
    db.init_app(app)
    migrate.init_app(app, db)
    from .models import User,CartItem,Seller,ProductCategory,Product,Order
    jwt.init_app(app)
    app.debug = True  # Enable debug mode
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({"message": "Welcome to the Home Page"}), 200
    from .controllers import register_all_routes
    register_all_routes(app)
    return app
