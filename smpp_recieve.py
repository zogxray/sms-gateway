import logging
import sys
import pprint

from smpplib import client

# if you want to know what's happening
logging.basicConfig(level='DEBUG')

client = client.Client('10.100.102.3', 7777)


def store_sms(pdu):
    print("*******************")
    print(str(pdu.source_addr))
    print(str(pdu.destination_addr))
    print(str(pdu.short_message.decode("utf-16-be")))

client.set_message_received_handler(
        lambda pdu: store_sms(pdu)
    )


client.connect()
client.bind_receiver(system_id='smpp01', password='smpp')

client.listen()
