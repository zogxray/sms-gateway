from flask import Flask, request
from flask_cors import CORS
from flask_orator import Orator, jsonify
from models.sms import Sms
from models.channel import Channel
from models.ussd import Ussd

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

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify({404: 'Page not found'})
@app.errorhandler(500)
def server_error(e):
    # note that we set the 404 status explicitly
    return jsonify({500: 'Oops. Something went wrong'})

@app.route('/channels/<int:id>/edit', methods=['GET'])
def channels_edit(id):
    channel = Channel.find(id)

    return jsonify(channel)

@app.route('/channels/<int:id>/update', methods=['POST'])
def channels_update(id):
    rdata = request.get_json()

    name = rdata.get('name', None)
    sim_id = rdata.get('sim_id', None)
    sim_pass = rdata.get('sim_pass', None)
    phone = rdata.get('phone', None)
    balance_ussd = rdata.get('balance_ussd', None)

    channel = Channel.find(id)
    channel.name = name
    channel.sim_id = sim_id
    channel.sim_pass = sim_pass
    channel.phone = phone
    channel.balance_ussd = balance_ussd
    channel.save()

    return jsonify(channel)

@app.route('/channels/add', methods=['POST'])
def channels_add():
    rdata = request.get_json()
    name = rdata.get('name', None)
    sim_id = rdata.get('sim_id', None)
    sim_pass = rdata.get('sim_pass', None)
    phone = rdata.get('phone', None)
    balance_ussd = rdata.get('balance_ussd', None)

    channel = Channel()
    channel.name = name
    channel.sim_id = sim_id
    channel.sim_pass = sim_pass
    channel.phone = phone
    channel.balance_ussd = balance_ussd
    channel.save()

    return jsonify(channel)

@app.route('/outgoing-sms/add', methods=['POST'])
def outgoing_sms_add():
    rdata = request.get_json()
    phone = rdata.get('phone', None)
    text = rdata.get('text', None)
    channel_id = rdata.get('channel_id', None)

    item = Sms()
    item.phone = phone
    item.text = text
    item.channel_id = channel_id
    item.direction = True
    item.save()

    return jsonify(item)

@app.route('/ussd/add', methods=['POST'])
def ussd_add():
    rdata = request.get_json()
    ussd = rdata.get('ussd', None)
    channel_id = rdata.get('channel_id', None)

    item = Ussd()
    item.ussd = ussd
    item.channel_id = channel_id
    item.save()

    return jsonify(item)

@app.route('/outgoing-sms/latest', methods=['POST'])
def outgoing_latest():
    rdata = request.get_json()
    date = rdata.get('date', None)
    sms = Sms.with_('channel').where('created_at', '>', date).where('direction', True).order_by('created_at', 'ASC').first()

    return jsonify(sms)

@app.route('/outgoing-sms/', methods=['POST', 'GET'])
@app.route('/outgoing-sms/<int:page>', methods=['POST', 'GET'])
def outgoing_sms(page=1):
    rdata = request.get_json()
    if rdata is None:
        text = None
    else:
        text = rdata.get('text', None)

    query = Sms.with_('channel').where('direction', True)

    if text is not None:
        query = query.where('text', 'like', '%' + text + '%')

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

@app.route('/ussd/', methods=['POST', 'GET'])
@app.route('/ussd/<int:page>', methods=['POST', 'GET'])
def ussd(page=1):
    rdata = request.get_json()
    if rdata is None:
        text = None
    else:
        text = rdata.get('text', None)

    query = Ussd.with_('channel')

    if text:
        query = query.where('answer', 'like', '%' + text + '%')

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

@app.route('/incoming-sms/latest', methods=['POST'])
def incoming_latest():
    rdata = request.get_json()
    date = rdata.get('date', None)
    sms = Sms.with_('channel').where('created_at', '>', date).where('direction', False).order_by('created_at', 'ASC').first()

    return jsonify(sms)

@app.route('/incoming-sms/', methods=['POST', 'GET'])
@app.route('/incoming-sms/<int:page>', methods=['POST', 'GET'])
def incoming_sms(page=1):
    rdata = request.get_json()
    if rdata is None:
        text = None
    else:
        text = rdata.get('text', None)

    query = Sms.with_('channel').where('direction', False)

    if text:
        query = query.where('text', 'like', '%' + text + '%')

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

    if text:
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

@app.route('/channels/all', methods=['GET'])
def channels_all():
    items = Channel.order_by('created_at', 'DESC').get()

    return jsonify(items)

@app.route('/trans.js', methods=['GET'])
def trans():
    return jsonify({'en': {
        'title': 'title'
    }})

if __name__ == "__main__":
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)
    app.run(host="0.0.0.0", port=5000, threaded=True)
