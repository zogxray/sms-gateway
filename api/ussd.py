from . import ussd
from security.token import require_token
from flask import request
from flask_orator import jsonify
from models.ussd import Ussd

@ussd.route('/ussd/add', methods=['POST'])
@require_token
def ussd_add():
    rdata = request.get_json()
    ussd = rdata.get('ussd', None)
    channel_id = rdata.get('channel_id', None)

    item = Ussd()
    item.ussd = ussd
    item.channel_id = channel_id
    item.save()

    return jsonify(item)

@ussd.route('/ussd/', methods=['POST', 'GET'])
@ussd.route('/ussd/<int:page>', methods=['POST', 'GET'])
@require_token
def ussds(page=1):
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
