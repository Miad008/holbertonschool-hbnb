from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

ns = Namespace("reviews", description="Review operations")
facade = HBnBFacade()

# Review model for input/output documentation
review_model = ns.model("Review", {
    "id": fields.String(description="Review ID"),
    "text": fields.String(required=True, description="Text of the review"),
    "rating": fields.Integer(required=True, description="Rating (1-5)", min=1, max=5),
    "user_id": fields.String(required=True, description="User ID"),
    "place_id": fields.String(required=True, description="Place ID")
})

@ns.route("/")
class ReviewList(Resource):
    @ns.marshal_list_with(review_model)
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

    @ns.expect(review_model, validate=True)
    @ns.marshal_with(review_model, code=201)
    @ns.response(400, "Invalid input")
    @ns.response(404, "User or place not found")
    def post(self):
        """Create a new review"""
        data = request.json

        user = facade.get_user(data.get("user_id"))
        if not user:
            ns.abort(404, "User not found")

        place = facade.get_place(data.get("place_id"))
        if not place:
            ns.abort(404, "Place not found")

        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            ns.abort(400, str(e))

@ns.route("/<string:review_id>")
class ReviewResource(Resource):
    @ns.marshal_with(review_model)
    @ns.response(404, "Review not found")
    def get(self, review_id):
        """Retrieve a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            ns.abort(404, "Review not found")
        return review.to_dict(), 200

    @ns.expect(review_model, validate=True)
    @ns.marshal_with(review_model)
    @ns.response(404, "Review not found")
    @ns.response(400, "Invalid input")
    def put(self, review_id):
        """Update a review"""
        data = request.json
        updated = facade.update_review(review_id, data)
        if not updated:
            ns.abort(404, "Review not found")
        return updated.to_dict(), 200

    @ns.response(200, "Review deleted successfully")
    @ns.response(404, "Review not found")
    def delete(self, review_id):
        """Delete a review"""
        deleted = facade.delete_review(review_id)
        if not deleted:
            ns.abort(404, "Review not found")
        return {"message": "Review deleted successfully"}, 200

@ns.route("/places/<string:place_id>/reviews")
class PlaceReviewList(Resource):
    @ns.response(200, "List of reviews retrieved successfully")
    @ns.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            ns.abort(404, "Place not found")
        reviews = facade.get_reviews_by_place(place_id)
        return [r.to_dict() for r in reviews], 200
