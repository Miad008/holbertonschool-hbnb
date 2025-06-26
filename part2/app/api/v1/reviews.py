from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

ns = Namespace("reviews", description="Review operations")
facade = HBnBFacade()

# Model used for input and output
review_model = ns.model("Review", {
    "text": fields.String(required=True, description="Text of the review"),
    "rating": fields.Integer(required=False, description="Rating from 1 to 5", min=1, max=5),
    "user_id": fields.String(required=True, description="User ID"),
    "place_id": fields.String(required=True, description="Place ID")
})

@ns.route("/")
class ReviewList(Resource):
    @ns.marshal_list_with(review_model)
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews]

    @ns.expect(review_model)
    @ns.marshal_with(review_model, code=201)
    def post(self):
        """Create a new review"""
        data = request.json

        # Validation: Check user and place exist
        user = facade.get_user(data.get("user_id"))
        if not user:
            ns.abort(400, "Invalid user_id")

        place = facade.get_place(data.get("place_id"))
        if not place:
            ns.abort(400, "Invalid place_id")

        try:
            new_review = facade.create_review(data)
            return new_review.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))


@ns.route("/<string:review_id>")
class ReviewResource(Resource):
    @ns.marshal_with(review_model)
    def get(self, review_id):
        """Retrieve a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            ns.abort(404, "Review not found")
        return review.to_dict()

    @ns.expect(review_model)
    @ns.marshal_with(review_model)
    def put(self, review_id):
        """Update a review"""
        data = request.json
        updated = facade.update_review(review_id, data)
        if not updated:
            ns.abort(404, "Review not found")
        return updated.to_dict()

    def delete(self, review_id):
        """Delete a review"""
        deleted = facade.delete_review(review_id)
        if not deleted:
            ns.abort(404, "Review not found")
        return {"message": "Review deleted successfully"}, 200


@ns.route("/places/<string:place_id>/reviews")
class PlaceReviewList(Resource):
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            ns.abort(404, "Place not found")
        reviews = facade.get_reviews_by_place(place_id)
        return [r.to_dict() for r in reviews], 200

