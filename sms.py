import socket
from models.sms import Sms
from models.channel import Channel
from app import db
import random
import time
import datetime
import re
from decimal import Decimal
from sys import getsizeof

while True:
    smses = Sms.with_('channel').where('direction', True).where('send_at', None).get()

    for sms in smses:
        channel_server = (sms.channel.address, sms.channel.port)
        sms.update(send_at=datetime.datetime.now())

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.SOL_UDP)
        sock.connect(channel_server)

        text_size = getsizeof(sms.text)

        message = 'MSG ' + str(sms.id) + ' ' + str(text_size) + ' ' + sms.text + '\n'
        message = message.encode('utf-8')
        sock.sendto(message, channel_server)

        payload, client_address = sock.recvfrom(1024)
        payload = payload.decode('utf-8')
        print(payload)

        password = payload.split(' ')[1]

        message = 'PASSWORD ' + str(sms.id) + ' ' + sms.channel.sim_pass + '\n'
        message = message.encode('utf-8')
        print(message)
        sock.sendto(message, channel_server)

        payload, client_address = sock.recvfrom(1024)
        payload = payload.decode('utf-8')
        print(payload)

        message = 'SEND ' + str(sms.id) + ' ' + str(sms.id) + ' ' + sms.phone + '\n'
        message = message.encode('utf-8')
        print(message)
        sock.sendto(message, channel_server)

        payload, client_address = sock.recvfrom(1024)
        payload = payload.decode('utf-8')
        print(payload)
        #
        # message = 'SEND ' + str(sms.id) + ' ' + str(sms.id+1) + ' ' + sms.phone + '\n'
        # message = message.encode('utf-8')
        # print(message)
        # sock.sendto(message, channel_server)
        #
        # payload, client_address = sock.recvfrom(1024)
        # payload = payload.decode('utf-8')
        # print(payload)

        message = 'DONE ' + str(sms.id) + '\n'
        message = message.encode('utf-8')
        print(message)
        sock.sendto(message, channel_server)

        payload, client_address = sock.recvfrom(1024)
        payload = payload.decode('utf-8')
        print(payload)

        sms.update(send_at=datetime.datetime.now())

    print('Sleep ' + str(datetime.datetime.now()))
    time.sleep(10)
