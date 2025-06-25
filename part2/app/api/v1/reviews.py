
from flask_restx import Namespace, Resource, fields
from flask import request
from app.core.facade import HBnBFacade

ns = Namespace("reviews", description="Review operations")
facade = HBnBFacade()

review_model = ns.model("Review", {
    'text': fields.String(required=True, description='Text of the review'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID')
    'rating': fields.Integer(required=False, min=1, max=5, description="Rating from 1 to 5")
})

@ns.route("/")
class ReviewList(Resource):
    @ns.marshal_list_with(review_model)
    def get(self):
        """List all reviews"""
        return [r.to_dict() for r in facade.get_all_reviews()]

    @ns.expect(review_model)
    @ns.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        return facade.create_review(request.json), 201

@ns.route("/<string:review_id>")
class ReviewResource(Resource):
    @ns.marshal_with(review_model)
    def get(self, review_id):
        """Get a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            ns.abort(404, "Review not found")
        return review

    @ns.expect(review_model)
    @ns.marshal_with(review_model)
    def put(self, review_id):
        """Update a review"""
        review = facade.update_review(review_id, request.json)
        if not review:
            ns.abort(404, "Review not found")
        return review

    def delete(self, review_id):
        """Delete a review"""
        deleted = facade.delete_review(review_id)
        if not deleted:
            ns.abort(404, "Review not found")
        return {"message": "Deleted"}, 200
