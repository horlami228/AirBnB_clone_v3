#!/usr/bin/python3

"""index script for routes"""
from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
import json

# create a route for status
@app_views.route("/status", methods=["GET"])
def show_status():
    return jsonify({'status': 'OK'})


@app_views.route("/stats", methods=["GET"])
def get_stats():
    """get stats about the data in database"""
    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }

    formated_json = json.dumps(stats, indent=2)
    return formated_json
