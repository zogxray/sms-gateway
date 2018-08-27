from flask import Flask, request
from flask_cors import CORS
from flask_orator import Orator, jsonify
from models.user import User
from datetime import datetime
from functools import wraps
import jwt
from api import auth
from api import trans
from api import channel
from api import sms
from api import ussd

import os
from os.path import join, dirname
from dotenv import load_dotenv

env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)


# Configuration
DEBUG = True
ORATOR_DATABASES = {
    'default': os.getenv('DEFAULT_CONNECTION'),
    'collector': {
        'driver': os.getenv('DEFAULT_CONNECTION_DRIVER'),
        'host': os.getenv('DEFAULT_CONNECTION_HOST'),
        'database': os.getenv('DEFAULT_CONNECTION_DATABASE'),
        'user': os.getenv('DEFAULT_CONNECTION_USER'),
        'password': os.getenv('DEFAULT_CONNECTION_PASSWORD'),
        'prefix': os.getenv('DEFAULT_CONNECTION_PREFIX')
    }
}

SECRET_KEY = os.getenv('SECRET_KEY')

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
            SECRET_KEY,
            algorithm='HS256'
        )

        return jwt_string

    except Exception as e:
        return str(e)


def decode_token(token):
    """Decodes the access token from the Authorization header."""
    try:
        payload = jwt.decode(token, SECRET_KEY)
        return payload['sub']

    except jwt.ExpiredSignatureError:
        return "Expired token. Please login to get a new token"

    except jwt.InvalidTokenError:
        return "Invalid token. Please register or login"


# Creating Flask application
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(__name__)

app.register_blueprint(auth)
app.register_blueprint(trans)
app.register_blueprint(channel)
app.register_blueprint(sms)
app.register_blueprint(ussd)

# Initializing Orator
db = Orator(app)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify({404: 'Page not found'})
@app.errorhandler(500)
def server_error(e):
    # note that we set the 404 status explicitly
    return jsonify({500: 'Oops. Something went wrong'})

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


if __name__ == "__main__":
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)
    app.run(host="0.0.0.0", port=5000, threaded=True)
