from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity  # Task 3 - JWT
from app.services.facade import HBnBFacade

# Create namespace and facade instance
ns = Namespace('users', description='User operations')
facade = HBnBFacade()

# Task 1: Password Hashing - Input model includes password
user_input_model = ns.model('UserInput', {
    'first_name': fields.String(required=True, description="User's first name"),
    'last_name': fields.String(required=True, description="User's last name"),
    'email': fields.String(required=True, description="User's email address"),
    'password': fields.String(required=True, description="User's password", min_length=8)  # Task 1
})

# Task 1: Password Hashing - Output model excludes password
user_output_model = ns.model('UserOutput', {
    'id': fields.String(description="User ID"),
    'first_name': fields.String(description="User's first name"),
    'last_name': fields.String(description="User's last name"),
    'email': fields.String(description="User's email address"),
    'is_admin': fields.Boolean(description="Admin status")
})

@ns.route('/')
class UserList(Resource):
    @ns.response(200, 'List of users retrieved successfully')
    @ns.marshal_list_with(user_output_model)  # Task 1
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200

    @ns.expect(user_input_model, validate=True)  # Task 1
    @ns.response(201, 'User created successfully')
    @ns.response(400, 'Email already registered')
    @ns.response(400, 'Invalid input data')
    @ns.marshal_with(user_output_model)  # Task 1
    def post(self):
        """Create a new user"""
        user_data = request.json

        # Task 1: Check if email is already used
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            ns.abort(400, "Email already registered")

        try:
            # Task 1: Password will be hashed inside the model
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))

@ns.route('/<string:user_id>')
@ns.param('user_id', 'User ID')
class UserItem(Resource):
    @ns.response(200, 'User details retrieved successfully')
    @ns.response(404, 'User not found')
    @ns.marshal_with(user_output_model)  # Task 1
    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            ns.abort(404, "User not found")
        return user.to_dict()

    @jwt_required()  # Task 3 - Require authentication
    @ns.expect(user_input_model, validate=True)  # Task 1
    @ns.response(200, 'User updated successfully')
    @ns.response(403, 'Unauthorized action')  # Task 3
    @ns.response(400, 'Invalid input data')   # Task 3
    @ns.response(404, 'User not found')
    @ns.marshal_with(user_output_model)  # Task 1
    def put(self, user_id):
        """Update a user's information"""
        # Task 3 - Authenticated User Access:
        # - Only the user can update their own profile
        # - Cannot modify email or password through this endpoint
        current_user_id = get_jwt_identity()
        if user_id != current_user_id:
            ns.abort(403, "Unauthorized action")

        user_data = request.json
        if "email" in user_data or "password" in user_data:
            ns.abort(400, "You cannot modify email or password")

        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            ns.abort(404, "User not found")
        return updated_user.to_dict(), 200
