#!/usr/bin/python3

"""index script for routes"""
from api.v1.views import app_views
from flask import jsonify

# create a route for status
@app_views.route("/status", methods=["GET"])
def show_status():
    return  jsonify({'status': 'OK'})
