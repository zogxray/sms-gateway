import logging
from smpplib.client import Client
from models.channel import Channel
from models.sms import Sms

import threading
import sys
from app import db

def store_sms(pdu, channel):
    message = str(pdu.short_message.decode("utf-16-be"))
    source_addres = str(pdu.source_addr.decode("utf-8"))
    print('store message  from '.join(source_addres).join(' ').join(source_addres))
    sms = Sms()
    sms.phone = source_addres
    sms.text = message
    sms.sim_msg_count = 0
    sms.channel_id = channel.id
    sms.save()

# if you want to know what's happening
logging.basicConfig(level='DEBUG')

channels = Channel.where('protocol', 'smpp').get()


clients = {}


def background(channel):
    print(channel.name)
    if channel.id not in clients:
        client = Client(channel.smpp_sim_address, channel.smpp_sim_port)
        client.set_message_received_handler(
            lambda pdu: store_sms(pdu, channel)
        )

        clients[channel.id] = client
    else:
        client = clients[channel.id]

    client.connect()
    client.bind_receiver(system_id=channel.smpp_sim_id, password=channel.smpp_sim_pass)

    while True:
        client.read_once()

print(channels)

for channel in channels:
    thread = threading.Thread(name=channel.id, target=background, args=([channel]))
    # thread.setDaemon(True)
    thread.start()
