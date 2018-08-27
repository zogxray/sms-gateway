import logging
from smpplib.client import Client
from models.channel import Channel
import threading
import sys
from app import db

def store_sms(pdu, channel):
    print("*******************")
    print(channel.id)
    print(channel.name)
    print("*******************")
    print(str(pdu.source_addr))
    print(str(pdu.destination_addr))
    print(str(pdu.short_message.decode("utf-16-be")))

# if you want to know what's happening
logging.basicConfig(level='DEBUG')

channels = Channel.where('protocol', 'smpp').get()

for channel in channels:
    print(channel.name)
    try:
        client = Client(channel.smpp_sim_address, channel.smpp_sim_port)
        client.set_message_received_handler(
                lambda pdu: store_sms(pdu, channel)
        )

        client.connect()
        client.bind_receiver(system_id=channel.smpp_sim_id, password=channel.smpp_sim_pass)

        # thread = threading.Thread(target=client.listen())
        # thread.setDaemon(True)
        # thread.start()
    except Exception as e:
        print(e)
        print("Connection error")
        sys.exit()

