#!/usr/bin/python3

"""script for users routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.user import User
from models import storage


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Get all User instances created"""
    all_users = []
    import_User = storage.all(User)  # get all User from storage
    """loop through to get all User instances and
    use the to_dict method to transform the objects to dictionary"""
    for value in import_User.values():
        dict = value.to_dict()
        all_users.append(dict)
    return make_response(jsonify(all_users), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_User():
    """making a post request"""
    """check if passed data was converted to JSON"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "password" not in request.get_json():
        abort(400, "Missing password")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    else:
        """initialize the new User object"""
        data = request.get_json()
        User_obj = User(**data)
        User_obj.save()
        """return the User object with a 201 status code"""
        responseObject = make_response(
            jsonify(User_obj.to_dict()), 201)
        return responseObject


@app_views.route("/users/<string:user_id>",
                 methods=["GET"], strict_slashes=False)
def get_one_user(user_id):
    """get one User instance by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route("/users/<string:user_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """delete object from storage"""
    user = storage.get(User, user_id)    # get object by id
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users/<string:user_id>",
                 methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """update an existing state instance by id"""

    if not request.get_json():
        abort(400, "Not a JSON")
    user = storage.get(User, user_id)    # get object by id
    if user is None:
        abort(404)
    data = request.get_json()
    """ update the state object with key-value pairs"""
    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
