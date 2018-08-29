from flask import request
from models.user import User
from datetime import datetime
from functools import wraps
from flask_orator import jsonify
import jwt

import os
def generate_token(user):
    """ Generates the access token"""
    try:
        payload = {
            'exp': user.expired_at,
            'iat': datetime.utcnow(),
            'sub': user.id
        }

        jwt_string = jwt.encode(
            payload,
            os.getenv('SECRET_KEY'),
            algorithm='HS256'
        )

        return jwt_string

    except Exception as e:
        return str(e)


def decode_token(token):
    """Decodes the access token from the Authorization header."""
    try:
        payload = jwt.decode(str(token), os.getenv('SECRET_KEY'))
        return payload['sub']

    except jwt.ExpiredSignatureError:
        return False

    except jwt.InvalidTokenError:
        return False

def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = {
            'message': 'Authorisation error. Invalid access token'
        }
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify(response), 401

        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = decode_token(access_token)
            user = User.find(user_id)
            if user:
                return func(*args, **kwargs)

            return jsonify(response), 401

    return wrapper