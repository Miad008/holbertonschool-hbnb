import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development config using SQLite"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///hbnb.db"
