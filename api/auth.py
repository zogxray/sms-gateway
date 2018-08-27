from flask import request
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_orator import jsonify
from app import generate_token
from . import auth

@auth.route('/login', methods=['POST'])
def login():
    rdata = request.get_json()
    login = rdata.get('login', None)
    password = rdata.get('password', None)

    user = User.where('login', login).first()

    if user and check_password_hash(user.password, password):
        expired_at = datetime.utcnow() + timedelta(hours=8)
        token = generate_token(user)

        user.update(token=token, expired_at=expired_at)
        return jsonify({'token': token})

    return jsonify({'error': 'User or password are incorrect'}), 401