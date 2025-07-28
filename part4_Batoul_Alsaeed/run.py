import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import create_app
from flask_restx import Api
from app.api.v1.users import ns as users_namespace, admin_ns as admin_users_namespace
from app.api.v1.auth import auth as auth_namespace
from app.api.v1.places import api as places_namespace
from app.api.v1.reviews import ns as reviews_namespace
from app.api.v1.auth import auth as auth_namespace
from app.api.v1.amenities import ns as amenities_namespace

app = create_app()
api = Api(app, title="HBnB API", version="1.0", description="HBnB REST API")

# Register all namespaces
api.add_namespace(users_namespace, path="/api/v1/users")
api.add_namespace(admin_users_namespace, path="/api/v1/admin_users")
api.add_namespace(places_namespace, path="/api/v1/places")
api.add_namespace(reviews_namespace, path="/api/v1/reviews")
api.add_namespace(auth_namespace, path="/api/v1/auth")  # Task 2: Login route
api.add_namespace(amenities_namespace, path="/api/v1/amenities")

if __name__ == "__main__":
    app.run(debug=True)
