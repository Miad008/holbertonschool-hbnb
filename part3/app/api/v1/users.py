from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt
)
from app.services.facade import HBnBFacade

# Facade
facade = HBnBFacade()

# === User Namespace ===
ns = Namespace('users', description='User operations')

# === Models ===
user_input_model = ns.model('UserInput', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True, min_length=8),
    'is_admin': fields.Boolean(required=False, description="Set user as admin (admin only)")
})

user_output_model = ns.model('UserOutput', {
    'id': fields.String(),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'email': fields.String(),
    'is_admin': fields.Boolean()
})

# === USER ROUTES ===
@ns.route('/')
class UserList(Resource):
    @ns.marshal_list_with(user_output_model)
    def get(self):
        """Get all users"""
        return [u.to_dict() for u in facade.get_all_users()], 200

    @ns.expect(user_input_model, validate=True)
    @ns.marshal_with(user_output_model)
    @ns.response(201, 'User created')
    @ns.response(400, 'Invalid or duplicate input')
    def post(self):
        """Register a new user (public)"""
        data = request.json
        if facade.get_user_by_email(data["email"]):
            ns.abort(400, "Email already registered")
        try:
            user = facade.create_user(data)
            return user.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route('/<string:user_id>')
@ns.param('user_id', 'User ID')
class UserItem(Resource):
    @ns.marshal_with(user_output_model)
    @ns.response(404, 'User not found')
    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            ns.abort(404, "User not found")
        return user.to_dict()

    @jwt_required()
    @ns.expect(user_input_model, validate=True)
    @ns.marshal_with(user_output_model)
    @ns.response(200, 'User updated')
    @ns.response(400, 'Cannot modify email/password here')
    @ns.response(403, 'Unauthorized')
    @ns.response(404, 'User not found')
    def put(self, user_id):
        """Update your user profile (excluding email/password)"""
        current_user_id = get_jwt_identity()
        if user_id != current_user_id:
            ns.abort(403, "Unauthorized action")

        data = request.json
        if "email" in data or "password" in data:
            ns.abort(400, "Cannot modify email or password here")

        user = facade.update_user(user_id, data)
        if not user:
            ns.abort(404, "User not found")
        return user.to_dict()


# === ADMIN ROUTES ===
admin_ns = Namespace("admin_users", description="Admin-only user management")

@admin_ns.route("/users")
class AdminUserCreate(Resource):
    @jwt_required()
    @admin_ns.expect(user_input_model, validate=True)
    @admin_ns.response(201, 'User created by admin')
    @admin_ns.response(403, 'Admin privileges required')
    @admin_ns.response(400, 'Bad request')
    def post(self):
        """Admin: create a user (including is_admin)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"message": "Admin privileges required"}, 403

        data = request.get_json()
        try:
            user = facade.create_user_admin(data)
            return user.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400


@admin_ns.route("/users/<string:user_id>")
@admin_ns.param('user_id', 'User ID')
class AdminUserUpdate(Resource):
    @jwt_required()
    @admin_ns.expect(user_input_model, validate=True)
    @admin_ns.response(200, 'User updated by admin')
    @admin_ns.response(403, 'Admin privileges required')
    @admin_ns.response(404, 'User not found')
    def put(self, user_id):
        """Admin: update any user (including email/password)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"message": "Admin privileges required"}, 403

        data = request.get_json()
        try:
            user = facade.update_user_admin(user_id, data)
            if not user:
                return {"message": "User not found"}, 404
            return user.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
