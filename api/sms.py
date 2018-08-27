from . import sms

from flask import request
from security.token import require_token
from flask_orator import jsonify
from models.sms import Sms


@sms.route('/outgoing-sms/add', methods=['POST'])
@require_token
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

@sms.route('/outgoing-sms/latest', methods=['POST'])
@require_token
def outgoing_latest():
    rdata = request.get_json()
    date = rdata.get('date', None)
    sms = Sms.with_('channel').where('created_at', '>', date).where('direction', True).order_by('created_at', 'ASC').first()

    return jsonify(sms)

@sms.route('/outgoing-sms/', methods=['POST', 'GET'])
@sms.route('/outgoing-sms/<int:page>', methods=['POST', 'GET'])
@require_token
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

@sms.route('/incoming-sms/latest', methods=['POST'])
@require_token
def incoming_latest():
    rdata = request.get_json()
    date = rdata.get('date', None)
    sms = Sms.with_('channel').where('created_at', '>', date).where('direction', False).order_by('created_at', 'ASC').first()

    return jsonify(sms)

@sms.route('/incoming-sms/', methods=['POST', 'GET'])
@sms.route('/incoming-sms/<int:page>', methods=['POST', 'GET'])
@require_token
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
