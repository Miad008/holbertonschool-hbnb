from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# Models
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenity IDs")
})

place_response_model = api.model('PlaceResponse', {
    'id': fields.String,
    'title': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'owner': fields.Nested(user_model),
    'amenities': fields.List(fields.Nested(amenity_model))
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.marshal_with(place_response_model, code=201)
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place (requires authentication)"""
        current_user = get_jwt_identity()
        user = facade.get_user(current_user["id"])
        if not user:
            api.abort(400, 'Authenticated user not found')

        data = request.json
        amenity_objs = []
        for amenity_id in data.get('amenities', []):
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                api.abort(400, f'Amenity with ID {amenity_id} not found')
            amenity_objs.append(amenity)

        data['owner'] = user
        data['amenities'] = amenity_objs

        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.marshal_with(place_response_model, as_list=True)
    def get(self):
        """Retrieve all places (public endpoint)"""
        places = facade.get_all_places()
        return [p.to_dict() for p in places]


@api.route('/<string:place_id>')
@api.param('place_id', 'Place ID')
class PlaceResource(Resource):
    @api.marshal_with(place_response_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (public endpoint)"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        return place.to_dict()

    @api.expect(place_model)
    @api.marshal_with(place_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information (owner or admin only)"""
        current_user = get_jwt_identity()
        claims = get_jwt()

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')

        is_admin = claims.get("is_admin", False)
        if not is_admin and str(place.owner.id) != current_user["id"]:
            api.abort(403, 'Unauthorized action')

        data = request.json
        amenity_objs = []
        for amenity_id in data.get('amenities', []):
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                api.abort(400, f'Amenity with ID {amenity_id} not found')
            amenity_objs.append(amenity)

        data['owner'] = place.owner
        data['amenities'] = amenity_objs

        try:
            updated_place = facade.update_place(place_id, data)
            return updated_place.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
