from flask import Blueprint, jsonify

from src.auth.authorize import authenticate

secret_blueprint = Blueprint('secret', __name__)


@secret_blueprint.route('/secure')
@authenticate
def secure():
    return jsonify({'data': 'Secure!'})
