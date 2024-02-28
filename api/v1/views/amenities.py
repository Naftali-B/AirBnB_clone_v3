#!/usr/bin/python3
"""Create a new view for Amenity objects that
handles all default RESTFul API actions"""

from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""

    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route("/amenities/<string:amenity_id>",
		methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an Amenity object"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<string:amenity_id>",
		methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an Amenity"""

    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>",
		methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object"""

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
