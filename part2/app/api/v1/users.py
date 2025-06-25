from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade  

# Create API namespace for user operations
ns = Namespace('users', description='User operations')
facade = HBnBFacade()

# User model schema (without password as required)
user_model = ns.model('User', {
    'first_name': fields.String(required=True, description="User's first name"),
    'last_name': fields.String(required=True, description="User's last name"),
    'email': fields.String(required=True, description="User's email address"),
})

@ns.route('/')
class UserList(Resource):
    @ns.marshal_list_with(user_model)
    def get(self):
        """Get all users (GET /users)"""
        users = facade.get_all_users()
        return [u.to_dict() for u in users]

    @ns.expect(user_model)
    @ns.response(201, 'User created successfully')
    @ns.response(400, 'Invalid input data')
    @ns.marshal_with(user_model)
    def post(self):
        """Create a new user (POST /users)"""
        user_data = request.json
        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))

@ns.route('/<string:user_id>')
@ns.param('user_id', 'User ID')
class UserItem(Resource):
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """Get a user by ID (GET /users/<id>)"""
        user = facade.get_user(user_id)
        if not user:
            ns.abort(404, "User not found")
        return user.to_dict()

    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, user_id):
        """Update user data (PUT /users/<id>)"""
        user_data = request.json
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            ns.abort(404, "User not found")
        return updated_user.to_dict()

    @ns.response(200, "User deleted successfully")
    def delete(self, user_id):
        """Delete user (DELETE /users/<id>)"""
        deleted = facade.delete_user(user_id)
        if deleted:
            return {"message": f"User {user_id} deleted."}
        ns.abort(404, f"User with id {user_id} not found.")
