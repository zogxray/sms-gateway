import logging
import sys

from smpplib import gsm
from smpplib import client
from smpplib import consts

# if you want to know what's happening
logging.basicConfig(level='DEBUG')

# Two parts, UCS2, SMS with UDH
parts, encoding_flag, msg_type_flag = gsm.make_parts(u'Test smpp!\n')

client = client.Client('10.100.102.3', 7777)

# Print when obtain message_id
client.set_message_sent_handler(
    lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))

client.connect()
client.bind_transceiver(system_id='smpp', password='smpp')

for part in parts:
    pdu = client.send_message(
        source_addr_ton=consts.SMPP_TON_INTL,
        #source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        # Make sure it is a byte string, not unicode:
        source_addr='+79896137584',

        dest_addr_ton=consts.SMPP_TON_INTL,
        #dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        # Make sure thease two params are byte strings, not unicode:
        destination_addr='+79896137573',
        short_message=part,

        data_coding=encoding_flag,
        esm_class=msg_type_flag,
        registered_delivery=True,
    )

    print(pdu.sequence)