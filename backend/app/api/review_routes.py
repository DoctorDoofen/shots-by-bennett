from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Review, db

review_routes = Blueprint('reviews', __name__)


# Create a review
@review_routes.route('/', methods=['POST'])
@login_required
def create_review():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return {"error": "Text is required"}, 400

    review = Review(
        text=text,
        user_id=current_user.id
    )
    db.session.add(review)
    db.session.commit()

    return jsonify(review.to_dict()), 201


# Get all reviews
@review_routes.route('/', methods=['GET'])
def get_all_reviews():
    reviews = Review.query.all()
    return jsonify([review.to_dict() for review in reviews])


# Get a single review by ID
@review_routes.route('/<int:id>', methods=['GET'])
def get_review(id):
    review = Review.query.get(id)
    if not review:
        return {"error": "Review not found"}, 404
    return jsonify(review.to_dict())


# Update a review
@review_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_review(id):
    review = Review.query.get(id)
    if not review:
        return {"error": "Review not found"}, 404
    if review.user_id != current_user.id:
        return {"error": "Unauthorized"}, 403

    data = request.get_json()
    review.text = data.get("text", review.text)

    db.session.commit()
    return jsonify(review.to_dict())


# Delete a review
@review_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_review(id):
    review = Review.query.get(id)
    if not review:
        return {"error": "Review not found"}, 404
    if review.user_id != current_user.id:
        return {"error": "Unauthorized"}, 403

    db.session.delete(review)
    db.session.commit()
    return {"message": "Review deleted"}


