from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

# Models for nested data
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

# Input model for creating/updating places
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenity IDs")
})

# Output model for responses (includes nested owner & amenities)
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
    def post(self):
        """Register a new place"""
        data = request.json
        owner = facade.get_user(data.get('owner_id'))
        if not owner:
            api.abort(400, 'Invalid owner_id')

        amenity_objs = []
        for amenity_id in data.get('amenities', []):
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                api.abort(400, f'Amenity with ID {amenity_id} not found')
            amenity_objs.append(amenity)

        data['owner'] = owner
        data['amenities'] = amenity_objs
        data.pop('owner_id')

        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.marshal_with(place_response_model, as_list=True)
    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return [p.to_dict() for p in places]


@api.route('/<string:place_id>')
@api.param('place_id', 'Place ID')
class PlaceResource(Resource):
    @api.marshal_with(place_response_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        return place.to_dict()

    @api.expect(place_model)
    @api.marshal_with(place_response_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        """Update a place's information"""
        if not facade.get_place(place_id):
            api.abort(404, 'Place not found')

        data = request.json
        owner = facade.get_user(data.get('owner_id'))
        if not owner:
            api.abort(400, 'Invalid owner_id')

        amenity_objs = []
        for amenity_id in data.get('amenities', []):
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                api.abort(400, f'Amenity with ID {amenity_id} not found')
            amenity_objs.append(amenity)

        data['owner'] = owner
        data['amenities'] = amenity_objs
        data.pop('owner_id')

        try:
            updated_place = facade.update_place(place_id, data)
            return updated_place.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
