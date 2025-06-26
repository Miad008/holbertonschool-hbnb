from flask import Flask
from flask_restx import Api
from .config import Config
  
# Import Namespaces
from app.api.v1.users import ns as users_ns
from app.api.v1.amenities import ns as amenities_ns
from app.api.v1.places import ns as places_ns
from app.api.v1.reviews import ns as reviews_ns

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
  
    # Setting up the Swagger interface
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='RESTful API for the HBnB platform',
        doc='/api/v1/'
    )

    # Namespaces registration
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
        
    return app
    
