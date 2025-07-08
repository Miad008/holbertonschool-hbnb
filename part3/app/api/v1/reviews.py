from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
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

    @jwt_required()
    @ns.expect(review_model, validate=True)
    @ns.marshal_with(review_model, code=201)
    @ns.response(400, "Invalid input")
    @ns.response(404, "User or place not found")
    @ns.response(403, "Unauthorized action")
    def post(self):
        """Create a new review"""
        data = request.json
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        if not is_admin and data["user_id"] != current_user_id:
            ns.abort(403, "You can only create reviews as yourself")

        user = facade.get_user(data.get("user_id"))
        if not user:
            ns.abort(404, "User not found")

        place = facade.get_place(data.get("place_id"))
        if not place:
            ns.abort(404, "Place not found")

        if not is_admin and place.owner.id == current_user_id:
            ns.abort(400, "You cannot review your own place")

        if not is_admin:
            existing_reviews = facade.get_reviews_by_place(data["place_id"])
            for r in existing_reviews:
                if r.user_id == current_user_id:
                    ns.abort(400, "You have already reviewed this place")

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

    @jwt_required()
    @ns.expect(review_model, validate=True)
    @ns.marshal_with(review_model)
    @ns.response(404, "Review not found")
    @ns.response(400, "Invalid input")
    @ns.response(403, "Unauthorized action")
    def put(self, review_id):
        """Update a review (owner or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            ns.abort(404, "Review not found")

        if not is_admin and review.user_id != current_user_id:
            ns.abort(403, "Unauthorized action")

        data = request.json
        updated = facade.update_review(review_id, data)
        return updated.to_dict(), 200

    @jwt_required()
    @ns.response(200, "Review deleted successfully")
    @ns.response(404, "Review not found")
    @ns.response(403, "Unauthorized action")
    def delete(self, review_id):
        """Delete a review (owner or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            ns.abort(404, "Review not found")

        if not is_admin and review.user_id != current_user_id:
            ns.abort(403, "Unauthorized action")

        deleted = facade.delete_review(review_id)
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
