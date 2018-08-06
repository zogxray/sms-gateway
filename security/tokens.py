import jwt
from datetime import datetime
from app import SECRET_KEY


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
