from flask import Flask
from .config import Config  # You can add your config file if needed

def create_app():
    # Create the Flask application instance
    app = Flask(__name__)
    
    # Load the configuration (optional, if you have a config file)
    app.config.from_object(Config)  # Adjust this based on your config setup
    
    # Register blueprints for the API routes
    from .api.v1.amenities import api as amenities_api
    from .api.v1.places import api as places_api
    from .api.v1.reviews import api as reviews_api
    
    app.register_blueprint(amenities_api, url_prefix='/api/v1/amenities')
    app.register_blueprint(places_api, url_prefix='/api/v1/places')
    app.register_blueprint(reviews_api, url_prefix='/api/v1/reviews')
    
    # Add any other app setup or extension registration (e.g., database, JWT)
    
    return app


