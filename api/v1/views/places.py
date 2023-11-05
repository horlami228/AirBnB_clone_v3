#!/usr/bin/python3

"""script for places routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route("/cities/<string:city_id>/places",
                 methods=["GET"], strict_slashes=False)
def get_all_places(city_id):
    """get all places by city id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    associated_places = [object.to_dict() for object in city.places]
    return jsonify(associated_places), 200


@app_views.route("/places/<string:place_id>", strict_slashes=False)
def get_one_place(place_id):
    """get one place instance by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route("/places/<string:place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """delete object from storage"""
    place = storage.get(Place, place_id)    # get object by id
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<string:city_id>/places",
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """create a new place instance"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")

    data = request.get_json()

    user = storage.get(User, data["user_id"])
    """check if user id is authentic"""
    if user is None:
        abort(404)

    data["city_id"] = city_id     # add city_id to data
    place = Place(**data)
    place.save()
    """return the place object with status code 201"""
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<string:place_id>",
                 methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """update an existing place instance"""
    place = storage.get(Place, place_id)   # get object by id
    if place is None:
        abort(404)

    if not request.get_json():  # not a valid json
        abort(400, "Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()  # commit changes to storage
    return make_response(jsonify(place.to_dict()), 200)
