import logging
import sys
import time
import datetime

from smpplib import gsm
from smpplib.client import Client
from smpplib import consts

from models.channel import Channel
from models.sms import Sms
from app import db

import threading

# if you want to know what's happening
logging.basicConfig(level='DEBUG')

channels = Channel.where('protocol', 'smpp').get()

def store_sms(pdu, sms):
    short_message = str(pdu.short_message.decode("utf-16-be"))
    source_addres = str(pdu.source_addr.decode("utf-8"))
    print('store message from '.join(source_addres).join(' ').join(short_message))
    sms.update(received_at=datetime.datetime.now())

def background(channel):
    while True:
        print('Check sms queue at' + str(datetime.datetime.now()))
        sms = Sms.with_('channel').where('direction', True).where('send_at', None).order_by('created_at', 'ASC').first()
        if sms:
            sms.update(send_at=datetime.datetime.now())
            # Two parts, UCS2, SMS with UDH
            parts, encoding_flag, msg_type_flag = gsm.make_parts(sms.text)
            client = Client(channel.smpp_sim_address, channel.smpp_sim_port)

            client.set_message_sent_handler(
                lambda pdu: store_sms(pdu, sms)
            )

            client.connect()
            client.bind_transceiver(system_id=channel.smpp_sim_id, password=channel.smpp_sim_pass)
            for part in parts:
                pdu = client.send_message(
                    source_addr_ton=consts.SMPP_TON_INTL,
                    # source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                    # Make sure it is a byte string, not unicode:
                    source_addr=channel.phone,

                    dest_addr_ton=consts.SMPP_TON_INTL,
                    # dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                    # Make sure thease two params are byte strings, not unicode:
                    destination_addr=sms.phone,
                    short_message=part,

                    data_coding=encoding_flag,
                    esm_class=msg_type_flag,
                    registered_delivery=True,
                )

                client.disconnect()

        time.sleep(5)


for channel in channels:
    thread = threading.Thread(name=channel.id, target=background, args=([channel]))
    # thread.setDaemon(True)
    thread.start()