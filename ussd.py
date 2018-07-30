import socket
from models.ussd import Ussd
from app import db

server_address = '127.0.0.1'
server_port = 44441
server = (server_address, server_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(server)

count_ussd = Ussd.where('send_at', None).count()

message = 'MSG 35435 343545 345345\n'
message = message.encode('utf-8')
sock.sendto(message, server)
payload = sock.recv(1024)
payload = payload.decode('utf-8')
print(payload)
