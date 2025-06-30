from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import DevelopmentConfig

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=DevelopmentConfig):
    """Application factory with config and extensions"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    return app
