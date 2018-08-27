from flask import Blueprint

auth = Blueprint('auth', __name__)
trans = Blueprint('trans', __name__)
channel = Blueprint('channel', __name__)
sms = Blueprint('sms', __name__)
ussd = Blueprint('ussd', __name__)

from api.auth import *
from api.trans import *
from api.channel import *
from api.sms import *
from api.ussd import *
