from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

# إنشاء Namespace للأماكن
ns = Namespace('places', description='Place operations')
facade = HBnBFacade()

# نموذج بيانات المكان
place_model = ns.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(required=True),
    'address': fields.String(required=True),
    'owner_id': fields.String(required=True),
    'price': fields.Float(required=False, default=0.0),
    'latitude': fields.Float(required=False, default=0.0),
    'longitude': fields.Float(required=False, default=0.0),
    'amenity_ids': fields.List(fields.String, required=False),
    'review_ids': fields.List(fields.String, required=False),
})

@ns.route('/')
class PlaceList(Resource):
    @ns.marshal_list_with(place_model)
    def get(self):
        """استعراض جميع الأماكن"""
        places = facade.get_all_places()
        return [p.to_dict() for p in places]

    @ns.expect(place_model)
    @ns.marshal_with(place_model, code=201)
    def post(self):
        """إنشاء مكان جديد"""
        place_data = request.json
        new_place = facade.create_place(place_data)
        return new_place.to_dict(), 201

@ns.route('/<string:place_id>')
@ns.param('place_id', 'Place ID')
class PlaceResource(Resource):
    @ns.marshal_with(place_model)
    def get(self, place_id):
        """استعراض مكان حسب ID"""
        place = facade.get_place(place_id)
        if place:
            return place.to_dict()
        ns.abort(404, f"Place with id {place_id} not found.")

    @ns.expect(place_model)
    @ns.marshal_with(place_model)
    def put(self, place_id):
        """تحديث بيانات مكان"""
        updates = request.json
        updated = facade.update_place(place_id, updates)
        if updated:
            return updated.to_dict()
        ns.abort(404, f"Place with id {place_id} not found.")
