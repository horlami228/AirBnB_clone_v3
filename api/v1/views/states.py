#!/usr/bin/python3

"""script for states routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Get all states instances created"""
    all_states = []
    import_states = storage.all(State)  # get all states from storage
    """loop through to get all states instances and
    use the to_dict method to transform the objects to dictionary"""
    for value in import_states.values():
        dict = value.to_dict()
        all_states.append(dict)
    return make_response(jsonify(all_states), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """making a post request"""
    """check if passed data was converted to JSON"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    else:
        """initialize the new state object"""
        data = request.get_json()
        state_obj = State(**data)
        state_obj.save()
        """resturn the state object with a 201 status code"""
        responseObject = make_response(
            jsonify(state_obj.to_dict()), 201)
        return responseObject


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=True)
def get_one_state(state_id):
    """get one state instance by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return make_response(jsonify(state.to_dict()), 200)


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=True)
def delete_state(state_id):
    """delete object from storage"""
    state = storage.get(State, state_id)    # get object by id
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=True)
def update_state(state_id):
    """update an existing state instance by id"""

    state = storage.get(State, state_id)    # get object by id
    if state is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    """ update the state object with key-value pairs"""
    for key, value in data.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        else:
            setattr(state, key, value)

    return make_response(jsonify(state.to_dict()), 200)
