from orator import Model
from orator.orm import belongs_to

class Ussd(Model):
    __table__ = 'ussd'
    __fillable__ = ['ussd', 'answer', 'send_at', 'channel_id', 'received_at']
    __dates__ = ['send_at', 'received_at']

    @belongs_to
    def channel(self):
        from models.channel import Channel
        return Channel