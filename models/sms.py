from orator import Model
from orator.orm import belongs_to

class Sms(Model):
    __table__ = 'sms'
    __fillable__ = ['phone', 'text', 'channel_id', 'sim_msg_count', 'direction', 'send_at', 'received_at']
    __dates__ = ['send_at', 'received_at']

    @belongs_to
    def channel(self):
        from models.channel import Channel
        return Channel