from orator import Model
from orator.orm import has_many

class Channel(Model):
    __table__ = 'channels'
    __fillable__ = ['name', 'phone', 'sim_id', 'sim_pass', 'balance', 'last_live_at', 'address', 'port', 'balance_ussd']
    __dates__ = ['created_at', 'updated_at', 'last_live_at']

    @has_many('channal_id', 'id')
    def sms(self):
        from models.sms import Sms
        return Sms.order_by('created_at', 'DESC')

    @has_many('channal_id', 'id')
    def sms(self):
        from models.ussd import Ussd
        return Ussd.order_by('created_at', 'DESC')
