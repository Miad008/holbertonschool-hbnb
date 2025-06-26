from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# Create namespace and facade instance
ns = Namespace('users', description='User operations')
facade = HBnBFacade()

# User model for validation and docs
user_model = ns.model('User', {
    'first_name': fields.String(required=True, description="User's first name"),
    'last_name': fields.String(required=True, description="User's last name"),
    'email': fields.String(required=True, description="User's email address"),
})

@ns.route('/')
class UserList(Resource):
    @ns.response(200, 'List of users retrieved successfully')
    @ns.marshal_list_with(user_model)
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200

    @ns.expect(user_model, validate=True)
    @ns.response(201, 'User created successfully')
    @ns.response(400, 'Email already registered')
    @ns.response(400, 'Invalid input data')
    @ns.marshal_with(user_model)
    def post(self):
        """Create a new user"""
        user_data = request.json

        # Check email uniqueness
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            ns.abort(400, "Email already registered")

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))

@ns.route('/<string:user_id>')
@ns.param('user_id', 'User ID')
class UserItem(Resource):
    @ns.response(200, 'User details retrieved successfully')
    @ns.response(404, 'User not found')
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            ns.abort(404, "User not found")
        return user.to_dict()

    @ns.expect(user_model, validate=True)
    @ns.response(200, 'User updated successfully')
    @ns.response(404, 'User not found')
    @ns.response(400, 'Invalid input data')
    @ns.marshal_with(user_model)
    def put(self, user_id):
        """Update a user's information"""
        user_data = request.json
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            ns.abort(404, "User not found")
        return updated_user.to_dict(), 200
