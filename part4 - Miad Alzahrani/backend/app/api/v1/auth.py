from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

# Namespace for authentication routes
auth = Namespace('auth', description='Authentication operations')
facade = HBnBFacade()

# Task 2: Login input model
login_model = auth.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@auth.route('/login')
class Login(Resource):
    @auth.expect(login_model)
    @auth.response(200, 'JWT token issued successfully')
    @auth.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = auth.payload

        # Step 1: Fetch user by email
        user = facade.get_user_by_email(credentials['email'])

        # Step 2: Verify password
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create JWT token with id and is_admin
        access_token = create_access_token(identity={
            'id': str(user.id),
            'is_admin': user.is_admin
        })

        # Step 4: Return the token
        return {'access_token': access_token}, 200

# Task 2: Protected route example
@auth.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @auth.response(200, 'Access granted')
    @auth.response(401, 'Missing or invalid token')
    def get(self):
        """A protected endpoint that requires JWT"""
        user = get_jwt_identity()
        return {
            'message': f'Hello, user {user["id"]}',
            'is_admin': user["is_admin"]
        }, 200
