#!/usr/bin/python3

"""script for reviews routes"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route("/places/<string:place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def get_all_reviews(place_id):
    """get all reviews by place id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    associated_reviews = [object.to_dict() for object in place.reviews]
    return jsonify(associated_reviews), 200


@app_views.route("/reviews/<string:review_id>", strict_slashes=False)
def get_one_review(review_id):
    """get one review instance by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return make_response(jsonify(review.to_dict()), 200)


@app_views.route("/reviews/<string:review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """delete object from storage"""
    review = storage.get(Review, review_id)    # get object by id
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<string:place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """create a new review instance"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "text" not in request.get_json():
        abort(400, "Missing text")
    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")

    data = request.get_json()

    user = storage.get(User, data["user_id"])
    """check if user id is authentic"""
    if user is None:
        abort(404)

    data["place_id"] = place_id     # add place_id to data
    review = Review(**data)
    review.save()
    """return the place object with status code 201"""
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<string:review_id>",
                 methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """update an existing review instance"""
    review = storage.get(Review, review_id)   # get object by id
    if review is None:
        abort(404)

    if not request.get_json():  # not a valid json
        abort(400, "Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    storage.save()  # commit changes to storage
    return make_response(jsonify(review.to_dict()), 200)
