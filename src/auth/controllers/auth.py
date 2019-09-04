from flask import Blueprint
from flask import request, jsonify

from src.auth.auth_exception import AccessDeniedException, UserNotFoundException
from src.auth.schemas.user_schema import UserSchema
from src.auth.schemas.login_schema import LoginSchema
from src.auth.services.auth_service import UserService
from src.jwt_handler import encode_data_to_jwt

user_schema = UserSchema()
login_schema = LoginSchema()

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    content = request.get_json()
    user_data = login_schema.load(content)
    service = UserService()
    try:
        user = service.get_user_by(
            field="username", value=user_data["username"], show_password=True
        )
    except UserNotFoundException as e:
        raise AccessDeniedException({"error": "User not found or wrong password"})

    is_valid = UserService.compare_password(
        hashed=user["password"],
        plain=user_data["password"]
    )

    if not is_valid:
        raise AccessDeniedException({"error": "User not found or wrong password"})

    del user["password"]

    token = get_user_token({
        "username": user["username"],
        "email": user["email"]
    })
    user.update({"token": token})
    return jsonify(user)


@auth_blueprint.route('/register', methods=['POST'])
def register():
    content = request.get_json()
    user_data = user_schema.load(content)
    service = UserService()
    user = service.create_user(user_data)
    token = get_user_token({
        "username": user["username"],
        "email": user["email"]
    })
    user.update({"token": token})
    return jsonify(user)


def get_user_token(user_data):
    return encode_data_to_jwt(user_data)
