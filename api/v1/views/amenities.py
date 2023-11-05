#!/usr/bin/python3

"""script for amentities routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Get all amenity instances created"""
    all_amenities = []
    import_amenity = storage.all(Amenity)  # get all amenity from storage
    """loop through to get all amenity instances and
    use the to_dict method to transform the objects to dictionary"""
    for value in import_amenity.values():
        dict = value.to_dict()
        all_amenities.append(dict)
    return make_response(jsonify(all_amenities), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """making a post request"""
    """check if passed data was converted to JSON"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    else:
        """initialize the new amenity object"""
        data = request.get_json()
        amenity_obj = Amenity(**data)
        amenity_obj.save()
        """resturn the amenity object with a 201 status code"""
        responseObject = make_response(
            jsonify(amenity_obj.to_dict()), 201)
        return responseObject


@app_views.route("/amenities/<string:amenity_id>",
                 methods=["GET"], strict_slashes=True)
def get_one_amenity(amenity_id):
    """get one amenity instance by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route("/amenities/<string:amenity_id>",
                 methods=["DELETE"], strict_slashes=True)
def delete_amenity(amenity_id):
    """delete object from storage"""
    amenity = storage.get(Amenity, amenity_id)    # get object by id
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities/<string:amenity_id>",
                 methods=["PUT"], strict_slashes=True)
def update_amenity(amenity_id):
    """update an existing state instance by id"""

    if not request.get_json():
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)    # get object by id
    if amenity is None:
        abort(404)
    data = request.get_json()
    """ update the state object with key-value pairs"""
    for key, value in data.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        else:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
