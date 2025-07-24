from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import HBnBFacade

facade = HBnBFacade()

ns = Namespace("amenities", description="Admin-only amenity management")

amenity_model = ns.model('Amenity', {
    'name': fields.String(required=True, description="Amenity name (max 50 characters)")
})

@ns.route('/')
class AmenityList(Resource):
    @jwt_required()
    @ns.expect(amenity_model, validate=True)
    @ns.response(201, "Amenity created")
    @ns.response(403, "Admin privileges required")
    def post(self):
        """Admin: create a new amenity"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"message": "Admin privileges required"}, 403

        data = request.get_json()
        try:
            amenity = facade.create_amenity(data)
            return amenity.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400


@ns.route('/<string:amenity_id>')
@ns.param('amenity_id', 'Amenity ID')
class AmenityItem(Resource):
    @jwt_required()
    @ns.expect(amenity_model, validate=True)
    @ns.response(200, "Amenity updated")
    @ns.response(403, "Admin privileges required")
    def put(self, amenity_id):
        """Admin: update an existing amenity"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"message": "Admin privileges required"}, 403

        data = request.get_json()
        try:
            amenity = facade.update_amenity(amenity_id, data)
            if not amenity:
                return {"message": "Amenity not found"}, 404
            return amenity.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
