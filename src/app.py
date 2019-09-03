import os
from flask import Flask, escape, request, jsonify
from marshmallow import ValidationError
from flask_pymongo import PyMongo

from src.auth.auth_exception import UserExistsException, UserNotFoundException, AccessDeniedException
from src.auth.controllers.auth import auth_blueprint

import src.settings

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get('MONGO_URL')

print(os.environ.get('MONGO_URL'))

mongo = PyMongo(app)

# set default version to v1
version = os.environ.get('API_VERSION', 'v1')
 
prefix = f"/api/{version}"


@app.errorhandler(ValidationError)
def validation_error_handler(err):
    errors = err.messages
    return jsonify(errors), 400


@app.errorhandler(UserExistsException)
def user_error_handler(e):
    return jsonify({"error": e.msg}), 400


@app.errorhandler(AccessDeniedException)
def user_error_handler(e):
    return jsonify({"error": e.msg}), 401


@app.errorhandler(UserNotFoundException)
def user_error_handler(e):
    return jsonify({"error": e.msg}), 404


app.register_blueprint(auth_blueprint, url_prefix=f'{prefix}/auth')


@app.route(f'{prefix}/ping', methods=['GET'])
def ping():
    """
        Check if server is alive
        :return: "pong"
    """
    return "pong"

