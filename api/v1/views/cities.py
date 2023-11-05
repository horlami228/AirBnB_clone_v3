#!/usr/bin/python3

"""script for city routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<string:state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def get_all_cities(state_id):
    """get all cities by state id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    associated_city = [object.to_dict() for object in state.cities]
    return jsonify(associated_city), 200


@app_views.route("/cities/<string:city_id>", strict_slashes=False)
def get_one_city(city_id):
    """get one city instance by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return make_response(jsonify(city.to_dict()), 200)


@app_views.route("/cities/<string:city_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """delete object from storage"""
    city = storage.get(City, city_id)    # get object by id
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<string:state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """create a new city instance"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    data = request.get_json()

    data["state_id"] = state_id     # add state_id to data
    city = City(**data)
    city.save()
    """return the city object with status code 201"""
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<string:city_id>",
                 methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """update an existing city instance"""
    city = storage.get(City, city_id)   # get object by id
    if city is None:
        abort(404)

    if not request.get_json():  # not a valid json
        abort(400, "Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()  # commit changes to storage
    return make_response(jsonify(city.to_dict()), 200)
