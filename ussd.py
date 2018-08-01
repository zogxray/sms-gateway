import socket
from models.ussd import Ussd
from models.channel import Channel
from app import db
import random
import time
import datetime
import re
from decimal import Decimal

while True:
    ussds = Ussd.with_('channel').where('received_at', None).get()

    for ussd in ussds:
        channel_server = (ussd.channel.address, ussd.channel.port)
        ussd.update(send_at=datetime.datetime.now())

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.SOL_UDP)
        sock.connect(channel_server)

        message = 'USSD ' + str(ussd.id) + ' ' + ussd.channel.sim_pass + ' ' + ussd.ussd
        print(message)
        message = message.encode('utf-8')
        sock.sendto(message, channel_server)

        payload, client_address = sock.recvfrom(1024)
        payload = payload.decode('utf-8')
        print(payload)
        ussd.update(answer=payload, received_at=datetime.datetime.now())

        if ussd.ussd == ussd.channel.balance_ussd:
            balance = re.findall('\d+[,.]\d+', payload)[0]
            isMinus = True if re.search(r'Минус', payload) else False
            if balance:
                balance = balance.replace(",", ".")
                if isMinus:
                    ussd.channel.update(balance=-abs(Decimal(balance)))
                else:
                    ussd.channel.update(balance=Decimal(balance))

    print('Sleep USSD 10 sec ' + str(datetime.datetime.now()))
    time.sleep(10)
