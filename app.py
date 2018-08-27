from flask import Flask, request
from flask_cors import CORS
from flask_orator import Orator, jsonify
from api import auth
from api import trans
from api import channel
from api import sms
from api import ussd

import os

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

if __name__ == "__main__":
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)
    app.run(host="0.0.0.0", port=5000, threaded=True)
