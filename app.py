from flask import Flask, request
from flask_cors import CORS
from flask_orator import Orator, jsonify
from models.sms import Sms
from models.channel import Channel

# Configuration
DEBUG = True
ORATOR_DATABASES = {
    'default': 'collector',
    'collector': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'collector',
        'user': 'root',
        'password': 'root',
        'prefix': ''
    }
}
SECRET_KEY = '4K5UA6+BMeyNPgYxhjFU03dYA1NlDGrf3wRr8uOcIHU='

# Creating Flask application
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(__name__)

# Initializing Orator
db = Orator(app)

@app.route('/channels/add', methods=['POST'])
def channels_add():
    rdata = request.get_json()
    name = rdata.get('name', None)
    sim_id = rdata.get('sim_id', None)
    sim_pass = rdata.get('sim_pass', None)
    phone = rdata.get('phone', None)

    channel = Channel()
    channel.name = name
    channel.sim_id = sim_id
    channel.sim_pass = sim_pass
    channel.phone = phone
    channel.save()

    return jsonify(channel)

@app.route('/sms/latest', methods=['POST'])
def sms_latest():
    rdata = request.get_json()
    date = rdata.get('date', None)
    sms = Sms.with_('channel').where('created_at', '>', date).order_by('created_at', 'ASC').first()

    return jsonify(sms)

@app.route('/sms/', methods=['POST', 'GET'])
@app.route('/sms/<int:page>', methods=['POST', 'GET'])
def sms(page=1):
    rdata = request.get_json()
    if rdata is None:
        text = None
    else:
        text = rdata.get('text', None)

    query = Sms.with_('channel')

    if text is not None:
        query = query.where('phone', 'like', '%' + text + '%').or_where('text', 'like', '%' + text + '%')

    items = query.order_by('created_at', 'DESC').paginate(25, page)

    data = {
        'data': items.serialize(),
        'total':  items.total,
        'per_page': items.per_page,
        'current_page': items.current_page,
        'last_page': items.last_page,
        'next_page_url': items.next_page,
        'prev_page_url': items.previous_page,
        'from': items.current_page*items.per_page-items.per_page,
        'to': items.current_page*items.per_page
    }

    return jsonify(data)

@app.route('/channels/', methods=['POST', 'GET'])
@app.route('/channels/<int:page>', methods=['POST', 'GET'])
def channels(page=1):
    rdata = request.get_json()
    if rdata is None:
        text = None
    else:
        text = rdata.get('text', None)

    query = Channel

    if text is not None:
        query = query.where('name', 'like', '%' + text + '%').or_where('phone', 'like', '%' + text + '%')

    items = query.order_by('created_at', 'DESC').paginate(25, page)

    data = {
        'data': items.serialize(),
        'total':  items.total,
        'per_page': items.per_page,
        'current_page': items.current_page,
        'last_page': items.last_page,
        'next_page_url': items.next_page,
        'prev_page_url': items.previous_page,
        'from': items.current_page*items.per_page-items.per_page,
        'to': items.current_page*items.per_page
    }

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
