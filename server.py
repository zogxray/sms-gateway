import socket
from models.sms import Sms
from models.channel import Channel
from app import db
import datetime
import time
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.SOL_UDP)
server_address = '0.0.0.0'
server_port = 44441
server = (server_address, server_port)
sock.bind(server)
print("Listening on " + server_address + ":" + str(server_port))

while True:
    payload, client_address = sock.recvfrom(1024)
    payload = payload.decode('utf-8')
    print(payload)
    rows = payload.split(";")
    request_data = {}
    for row in rows:
        rowd = row.split(":")
        request_data[rowd[0]] = rowd[-1]

    if 'req' in request_data:
        channel = Channel.where('sim_id', request_data['id']).where('sim_pass', request_data['pass']).first()
        if channel is None:
            message = 'RECEIVE ' + request_data['RECEIVE'] + 'ERROR Channel not found at SMA - hub'
            message = message.encode('utf-8')

        channel.update(address=client_address[0], port=client_address[1], last_live_at=datetime.datetime.now())

        message = 'Keep-Alive request ' + request_data['req'] + '\n'
        print('Keep-Alive request '.join(request_data['req']))
        message = 'reg:'+request_data['req']+';status:0;'
        message = message.encode('utf-8')

        sock.sendto(message, client_address)

    if 'RECEIVE' in request_data:
        channel = Channel.where('sim_id', request_data['id']).where('sim_pass', request_data['password']).first()

        message = 'RECEIVE message ' +request_data['RECEIVE']+ ' from ' +request_data['id'] + '\n'
        print(message)

        if channel is None:
            message = 'RECEIVE ' + request_data['RECEIVE'] + 'ERROR Channel not found at SMA - hub'
            message = message.encode('utf-8')

            sock.sendto(message, client_address)
        else:
            sms = Sms()
            sms.phone = request_data['srcnum']
            sms.text = request_data['msg']
            sms.sim_msg_count = request_data['RECEIVE']
            sms.channel_id = channel.id
            sms.save()

            message = 'RECEIVE ' + request_data['RECEIVE'] + 'OK\n'
            message = message.encode('utf-8')

            sock.sendto(message, client_address)
