#!/usr/bin/python3

"""Flask application"""
from flask import Flask, jsonify
from models import storage
import os
from api.v1.views import app_views

# initialize a new flask application
app = Flask(__name__)
# register our blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def shutdown_session(exception=None):
    """perform cleanup when app is shutdown"""
    storage.close()


@app.errorhandler(404)
def not_found_error(err):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    try:
        host_conn = os.getenv("HBNB_API_HOST")
        if host_conn is None:
            host_conn = "0.0.0.0"
        port_conn = os.getenv("HBNB_API_PORT")
        if port_conn is None:
            port_conn = 5000
    except Exception:
        pass
    print(app.url_map)
    app.run(host=host_conn, port=port_conn, threaded=True)
