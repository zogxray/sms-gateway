from . import channel
from flask import request
from security.token import require_token
from flask_orator import jsonify
from models.channel import Channel

@channel.route('/channel/<int:id>', methods=['GET'])
@require_token
def channels_edit(id):
    channel = Channel.find(id)

    return jsonify(channel)

@channel.route('/channels/<int:id>/update', methods=['POST'])
@require_token
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

@channel.route('/channels/add', methods=['POST'])
@require_token
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

@channel.route('/channels/', methods=['POST', 'GET'])
@channel.route('/channels/<int:page>', methods=['POST', 'GET'])
@require_token
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

@channel.route('/channels/all', methods=['GET'])
@require_token
def channels_all():
    items = Channel.order_by('created_at', 'DESC').get()

    return jsonify(items)