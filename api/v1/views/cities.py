#!/usr/bin/python3
"""Create a new view for City objects that
handles all default RESTFul API actions"""

from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage


@app_views.route("/states/<string:state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):

    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<string:city_id>",
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):

    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<string:city_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):

    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route("/states/<string:state_id>/cities",
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):

    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        return (jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    if 'name' not in data:
        return (jsonify({'error': 'Missing name'}), 400)
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<string:city_id>",
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):

    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        return (jsonify({'error': 'Not a JSON'}), 400)
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
