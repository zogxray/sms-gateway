from flask import Flask, request
from flask_cors import CORS
from flask_orator import Orator, jsonify
from models.sms import Sms
from models.channel import Channel
from models.ussd import Ussd
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from security import tokens
from functools import wraps

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
            user_id = tokens.decode_token(access_token)
            user = User.find(user_id)
            if user:
                return func(*args, **kwargs)

            return jsonify(response), 401

    return wrapper

@app.route('/channel/<int:id>', methods=['GET'])
@require_token
def channels_edit(id):
    channel = Channel.find(id)

    return jsonify(channel)

@app.route('/channels/<int:id>/update', methods=['POST'])
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

@app.route('/channels/add', methods=['POST'])
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

@app.route('/outgoing-sms/add', methods=['POST'])
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

@app.route('/ussd/add', methods=['POST'])
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

@app.route('/outgoing-sms/latest', methods=['POST'])
@require_token
def outgoing_latest():
    rdata = request.get_json()
    date = rdata.get('date', None)
    sms = Sms.with_('channel').where('created_at', '>', date).where('direction', True).order_by('created_at', 'ASC').first()

    return jsonify(sms)

@app.route('/outgoing-sms/', methods=['POST', 'GET'])
@app.route('/outgoing-sms/<int:page>', methods=['POST', 'GET'])
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

@app.route('/ussd/', methods=['POST', 'GET'])
@app.route('/ussd/<int:page>', methods=['POST', 'GET'])
@require_token
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
@require_token
def incoming_latest():
    rdata = request.get_json()
    date = rdata.get('date', None)
    sms = Sms.with_('channel').where('created_at', '>', date).where('direction', False).order_by('created_at', 'ASC').first()

    return jsonify(sms)

@app.route('/incoming-sms/', methods=['POST', 'GET'])
@app.route('/incoming-sms/<int:page>', methods=['POST', 'GET'])
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

@app.route('/channels/', methods=['POST', 'GET'])
@app.route('/channels/<int:page>', methods=['POST', 'GET'])
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

@app.route('/channels/all', methods=['GET'])
@require_token
def channels_all():
    items = Channel.order_by('created_at', 'DESC').get()

    return jsonify(items)

@app.route('/lang.js', methods=['GET'])
def lang():
    return jsonify(
        {
            'en': {
                'title': 'SMS-gateway',
                'incomingSms': 'Incoming Sms',
                'outgoingSms': 'Outgoing Sms',
                'sendSms': 'Send Sms',
                'ussd': 'USSD',
                'sendUssd': 'Send USSD',
                'simCarts': 'SIM carts',
                'simCart': 'SIM cart',
                'addSim': 'Create SIM',
                'updateSim': 'Update SIM',
                'phone': 'Phone',
                'text': 'Text',
                'receivedAt': 'Received at',
                'errorLabel': 'Whoops!',
                'errorDescription': 'Something went wrong.',
                'notFoundLabel': 'Not found!',
                'notFoundDescription': 'No found. Try a different search term.',
                'search': 'Search...',
                'id': 'ID',
                'createdAt': 'Created at',
                'requestSentAt': 'Request sent at',
                'requestReceivedAt': 'Request received at',
                'ussdRequest': 'USSD request',
                'ussdAnswer': 'USSD answer',
                'name': 'Name',
                'balance': 'Balance',
                'edit': 'Edit',
                'sim_id': 'SIM ID of channel',
                'sim_pass': 'SIM key of channel',
                'last_live_at': 'Last activity',
                'channel_warring': 'The transmitting channel must be configured on the GoIP device. The Activity field in the channel list will show the date of the last request from device',
                'ussd_balance': 'USSD to balance check',
                'form.name.required': 'Name is required',
                'form.sim_id.required': 'SIM ID is required',
                'form.sim_pass.required': 'SIM pass is required',
                'form.phone.required': 'Phone is required',
                'form.balance_ussd.required': 'Balance is required',
                'channel_id': 'Channel ID',
                'form.channel_id.required': 'Channel ID is required',
                'form.ussd.required': 'USSD is required',
                'form.text.required': 'Text is required',
                'check_balance': 'Check',
            },
            'ru': {
                'title': 'SMS-шлюз',
                'incomingSms': 'Входящие Sms',
                'outgoingSms': 'Исходящие Sms',
                'sendSms': 'Отправить Sms',
                'ussd': 'USSD',
                'sendUssd': 'Отправить USSD',
                'simCarts': 'SIM карты',
                'simCart': 'SIM карта',
                'addSim': 'Добавить SIM',
                'updateSim': 'Изменить SIM',
                'phone': 'Телефон',
                'text': 'Текст',
                'receivedAt': 'Дата получения',
                'errorLabel': 'Упс!',
                'errorDescription': 'Что-то пошло не так.',
                'notFoundLabel': 'Не найдено!',
                'notFoundDescription': 'Не найдено. Попробуйте другой поисковый запрос.',
                'search': 'Поиск...',
                'id': 'ID',
                'createdAt': 'Дата создания',
                'requestSentAt': 'Запрос отправлен',
                'requestReceivedAt': 'Запрос получен',
                'ussdRequest': 'USSD запрос',
                'ussdAnswer': 'USSD ответ',
                'name': 'Название',
                'balance': 'Баланс',
                'edit': 'Изменить',
                'sim_id': 'SIM ID канала',
                'sim_pass': 'SIM ключ канала',
                'last_live_at': 'Последняя активность',
                'channel_warring': 'Передающий канал должен быть настроен на GoIP устройстве. Поле активность в списке каналов покажет дату последнего запроса с утройства',
                'ussd_balance': 'USSD проверки баланса',
                'form.name.required': 'Название обязательно для заполнения',
                'form.sim_id.required': 'ID обязателен для заполнения',
                'form.sim_pass.required': 'Ключ обязателен для заполнения',
                'form.phone.required': 'Телефон обязателен для заполнения',
                'form.balance_ussd.required': 'USSD проверки баланса обязателен для заполнения',
                'channel_id': 'ID канала',
                'form.channel_id.required': 'ID канала обязателен для заполнения',
                'form.ussd.required': 'USDD обязателен для заполнения',
                'form.text.required': 'Текст обязателен для заполнения',
                'check_balance': 'Проверить',
            }
        }
    )

@app.route('/login', methods=['POST'])
def login():
    rdata = request.get_json()
    login = rdata.get('login', None)
    password = rdata.get('password', None)

    user = User.where('login', login).first()

    if user and check_password_hash(user.password, password):
        expired_at = datetime.utcnow() + timedelta(hours=8)
        token = tokens.generate_token(user)

        user.update(token=token, expired_at=expired_at)
        return jsonify({'token': token})

    return jsonify({'error': 'User or password are incorrect'}), 401

if __name__ == "__main__":
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)
    app.run(host="0.0.0.0", port=5000, threaded=True)
