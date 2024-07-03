import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:Aeduardo_0500@kernar.pythonanywhere.com./mysite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
