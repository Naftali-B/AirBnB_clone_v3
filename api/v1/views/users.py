#!/usr/bin/python3
"""Create a new view for User objects that
handles all default RESTFul API actions"""

from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route("/users/<string:user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    if not request.is_json:
        return (jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    if 'email' not in data:
        return (jsonify({'error': 'Missing email'}), 400)
    if 'password' not in data:
        return (jsonify({'error': 'Missing password'}), 400)
    user = User(**data)
    user.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route("/users/<string:user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        return (jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
