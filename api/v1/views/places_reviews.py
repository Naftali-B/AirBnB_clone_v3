#!/usr/bin/python3
"""Create a new view for Review objects that
handles all default RESTFul API actions"""

from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route("/places/<string:place_id>/reviews",
		methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieves the list of all Review objects of a Place"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<string:review_id>",
		methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<string:review_id>",
		methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route("/places/<string:place_id>/reviews",
		methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        return (jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    if 'user_id' not in data:
        return (jsonify({'error': 'Missing user_id'}), 400)
    user_id = data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'text' not in data:
        return (jsonify({'error': 'Missing text'}), 400)
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<string:review_id>",
		methods=['PUT'], strict_slashes=False)
def update_review(review_id):

    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.is_json:
        return (jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
