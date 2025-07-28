from app import create_app
from app.api.v1.users import ns as users_namespace, admin_ns as admin_users_namespace
from app.api.v1.auth import auth as auth_namespace  # Task 2: JWT login namespace
from flask_restx import Api

app = create_app()
api = Api(app, title="HBnB API", version="1.0", description="HBnB REST API")

# Register all namespaces
api.add_namespace(users_namespace, path="/api/v1/users")
api.add_namespace(auth_namespace, path="/api/v1/auth")  # Task 2: Login route

if __name__ == "__main__":
    app.run(debug=True)
