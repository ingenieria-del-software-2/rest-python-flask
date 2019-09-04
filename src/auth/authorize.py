from flask import Response, request
from functools import wraps
from src.jwt_handler import decode_jwt_data
from src.auth.services.auth_service import UserService, UserNotFoundException
import jwt


def valid_credentials(username, password):
    from src.app import app
    return username == app.config['USER'] and password == app.config['PASS']


def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        import pdb;pdb.set_trace()
        auth = request.headers['Authorization']
        way, token = auth.split()
        if way != "Bearer" or not is_valid_token(token):
            return Response('Login!', 401, {'WWW-Authenticate': 'Basic realm="Login!"'})
        return f(*args, **kwargs)
    return wrapper


def is_valid_token(token):
    try:
        user_data = decode_jwt_data(token)
        service = UserService()
        user = service.get_user_by("username", user_data["username"])
        return user is not None
    except jwt.exceptions.DecodeError:
        return False
    except UserNotFoundException:
        return False



