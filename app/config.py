import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:Laxman52962@localhost/ecom")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Laxman1234'
    JWT_SECRET_KEY = 'Laxman1234'