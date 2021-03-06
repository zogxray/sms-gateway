from flask import Flask, request
from flask_cors import CORS
from flask_orator import Orator, jsonify
from api import auth
from api import trans
from api import channel
from api import sms
from api import ussd

from os.path import join, dirname
from dotenv import load_dotenv
from raven import Client

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
import os

client = Client(os.getenv('SENTRY_KEY'))

# Configuration
DEBUG = True

ORATOR_DATABASES = {
    'default': os.getenv('DEFAULT_CONNECTION'),
    os.getenv('DEFAULT_CONNECTION'): {
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

@app.errorhandler(Exception)
def all_exception_handler(error):
    client.captureException()
    return jsonify({500: 'Oops. Something went wrong'}), 500

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    client.captureException()
    return jsonify({404: 'Page not found'}), 404

@app.errorhandler(404)
def page_not_authorize(e):
    # note that we set the 404 status explicitly
    client.captureException()
    return jsonify({401: 'Not authorize'}), 401

if __name__ == "__main__":
    app.register_error_handler(Exception, all_exception_handler)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(401, page_not_authorize)
    app.run(host="0.0.0.0", port=5000, threaded=True)
