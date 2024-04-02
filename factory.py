from flask import Flask
from database import db, init_db
from models import Episodes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///happy_little.db'
    init_db(app)
    return app