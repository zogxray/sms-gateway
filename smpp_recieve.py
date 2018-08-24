import logging
import sys

from smpplib import gsm
from smpplib import client
from smpplib import consts

# if you want to know what's happening
# logging.basicConfig(level='DEBUG')

client = client.Client('10.100.102.3', 7777)

# Print when obtain message_id
client.set_message_sent_handler(
    lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
client.set_message_received_handler(
    lambda pdu: sys.stdout.write('delivered {} {} {}\n'.format(pdu.short_message.decode("utf-16"), pdu.short_message.decode("utf-7"), pdu.short_message.decode("utf-16-be"))))

client.connect()
client.bind_receiver(system_id='smpp', password='smpp')

client.listen()