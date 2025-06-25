from flask import request
from flask_restx import Namespace, Resource, fields
from app.core.facade import HBnBFacade

ns = Namespace('amenities', description='Amenity operations')
facade = HBnBFacade()

amenity_model = ns.model('Amenity', {
    'name': fields.String(required=True),
    'description': fields.String(required=False),
})

@ns.route('/')
class AmenityList(Resource):
    @ns.marshal_list_with(amenity_model)
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities]

    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = request.json
        new_amenity = facade.create_amenity(data)
        return new_amenity.to_dict(), 201

@ns.route('/<string:amenity_id>')
@ns.param('amenity_id', 'Amenity ID')
class AmenityResource(Resource):
    @ns.marshal_with(amenity_model)
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if amenity:
            return amenity.to_dict()
        ns.abort(404, f"Amenity with id {amenity_id} not found.")

    @ns.expect(amenity_model)
    @ns.marshal_with(amenity_model)
    def put(self, amenity_id):
        data = request.json
        updated = facade.update_amenity(amenity_id, data)
        if updated:
            return updated.to_dict()
        ns.abort(404, f"Amenity with id {amenity_id} not found.")
